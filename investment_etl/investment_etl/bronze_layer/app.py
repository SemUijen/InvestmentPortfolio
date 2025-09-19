"""Main application for the Spark ETL process of the Bronze Layer."""

import asyncio
import logging
import os
from datetime import UTC, datetime

import pyarrow as pa
import pyarrow.compute as pc
from dotenv import load_dotenv

from investment_etl.silver_layer.tables.deltalake_tables import (
    InvestmentOptionValueOvertime,
    IoStockExchange,
)

from .stockprobe.alphavantage.url_generator import (
    ExchangeSymbols,
    ForeignExchangeRateURL,
    OutputSizeEnum,
    TimeSeriesDailyURL,
)
from .utils import AsyncDataIngestor, IngestionURL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

MAX_DIFFERENCE_DAYS = 90


def get_investment_options() -> dict[str, dict[str, str]]:
    """Retrieve investment options from the Delta Lake table."""

    def _get_symbols() -> dict[str, dict[str, str]] | None:
        dt = IoStockExchange().get_table().to_pyarrow_table()

        # NOTE: we use 'max' to get a single exchange symbol
        # per investment option it doesnt matter for this case
        grouped = dt.group_by("io_symbol").aggregate([("exchange_symbol", "max")])

        # Return a dictionary: {io_symbol: exchange_symbol}
        return {
            str(symbol): {"exchange_symbol": str(exchange_symbol)}
            for symbol, exchange_symbol in zip(
                grouped["io_symbol"].to_pylist(),
                grouped["exchange_symbol_max"].to_pylist(),
                strict=True,
            )
        }

    def _get_output_size_per_symbol(
        symbols: dict[str, dict[str, str]],
    ) -> dict[str, dict[str, str]]:
        dt = InvestmentOptionValueOvertime().get_table().to_pyarrow_table()

        for symbol, symbol_info in symbols.items():
            filtered = dt.filter(pc.equal(dt["symbol"], pa.scalar(symbol)))

            max_date_py = pc.max(filtered["date"]).as_py()
            if not isinstance(max_date_py, datetime) or max_date_py is None:
                symbol_info["output_size"] = OutputSizeEnum.FULL
            else:
                # Use timezone-aware datetime for comparison
                today = datetime.now(tz=UTC).date()
                max_date_date = max_date_py.date()
                if (today - max_date_date).days > MAX_DIFFERENCE_DAYS:
                    symbol_info["output_size"] = OutputSizeEnum.FULL
                else:
                    symbol_info["output_size"] = OutputSizeEnum.COMPACT

        return symbols

    symbols = _get_symbols()
    if not symbols:
        msg = "No symbols found in the database"
        raise ValueError(msg)

    logger.info("Symbols found: %s", symbols)

    return _get_output_size_per_symbol(symbols)


async def main() -> None:
    """Execute Bronze Extractions."""
    # Example URLs and symbol names
    load_dotenv()

    symbols = get_investment_options()

    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        error_message = "No API key found. Please set the API_KEY environment variable."
        raise ValueError(error_message)

    urls_to_ingest = []
    urls_to_ingest = [
        (
            IngestionURL(
                url=TimeSeriesDailyURL(
                    apikey=api_key,
                    symbol=symbol + "." + symbol_info["exchange_symbol"],
                    outputsize=OutputSizeEnum(symbol_info["output_size"]),
                ).return_url(),
                api_category="investment_options",
                name=symbol,
            )
        )
        for symbol, symbol_info in symbols.items()
    ]

    # add foreign exchange rate URL:
    urls_to_ingest.append(
        (
            IngestionURL(
                url=ForeignExchangeRateURL(
                    apikey=api_key,
                    from_symbol=ExchangeSymbols.USD,
                    to_symbol=ExchangeSymbols.EURO,
                ).return_url(),
                api_category="exchange_rate",
                name="USD_EUR",
            )
        ),
    )

    data_dir = os.getenv("DATA_DIR", "")
    if not data_dir:
        msg = "DATA_DIR environment variable is not set."
        raise ValueError(msg)

    # Create ingestor
    ingestor = AsyncDataIngestor(
        to_ingest=urls_to_ingest,
        base_dir=rf"{data_dir}/bronze",
        semaphore=2,
    )

    # Run ingestion
    await ingestor.ingest_all()


if __name__ == "__main__":
    asyncio.run(main())
