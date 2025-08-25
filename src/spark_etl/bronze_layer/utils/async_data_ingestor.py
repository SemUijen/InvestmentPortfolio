import asyncio
import json
import logging
from datetime import date
from pathlib import Path

import aiofiles
import aiohttp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


class APIRateLimitError(Exception):
    """Custom exception for API rate limit errors."""

    def __init__(self):
        super().__init__()
        self.message = "API rate limit exceeded."


class AsyncDataIngestor:
    """Asynchronous data ingestor for fetching data from a URL."""

    def __init__(
        self,
        to_ingest: list[tuple[str, str]],
        base_dir: str,
        semaphore: int = 5,
    ) -> None:
        self.semaphore = asyncio.Semaphore(semaphore)
        self.to_ingest = to_ingest
        self.base_dir = base_dir

    async def fetch_data(self, url: str) -> dict:
        """Fetch data from the URL asynchronously."""
        async with (
            self.semaphore,
            aiohttp.ClientSession() as session,
            session.get(
                url,
            ) as response,
        ):
            logger.info("Status %s", response.status)
            # NOTE: if API key limit is reached, API will not return an error
            # but an empty response
            response.raise_for_status()  # Raise an error for bad responses

            response_data = await response.json()
            if (
                "our standard API rate limit is 25 requests per day"
                in response_data.get("Information", "notfound")
            ):
                logger.error("API limit reached")
                raise APIRateLimitError

            return await response.json()

    async def save_data(self, data: dict, file_path: str) -> None:
        """Save the fetched data to a file."""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, "w") as file:
            await file.write(json.dumps(data, indent=4))
            logger.info("Data saved to %s", file_path)

    async def ingest(self, url: str, symbol_name: str) -> Exception | None:
        """Ingest data from the URL and save it to a file."""
        try:
            logger.info("Starting data ingestion for %s", symbol_name)
            response = await self.fetch_data(url=url)

            file_path = await self.create_file_path(symbol_name)
            await self.save_data(response, file_path)
            logger.info("Data ingestion completed successfully.")
        except Exception as e:
            logger.exception("Error during data ingestion for %s: %s", symbol_name, e)
            return e
        else:
            return None

    async def create_file_path(self, symbol_name: str) -> str:
        """Create a file path for saving data."""
        today = date.today()
        symbol_name = symbol_name.split(".")[0]  # Remove exchange suffix if present
        file_name = f"{today}_{symbol_name}.json"
        directory = (
            Path(self.base_dir)
            / "investment_options"
            / symbol_name
            / f"year={today.year}"
            / f"month={today.month}"
            / f"day={today.day}"
        )
        return rf"{directory}/{file_name}"

    async def ingest_all(self) -> None:
        """Ingest data from all URLs concurrently."""
        tasks = []
        for url, symbol_name in self.to_ingest:
            task = self.ingest(url, symbol_name)
            tasks.append(task)

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        if any(isinstance(result, Exception) for result in results):
            logger.error("Some ingestion tasks failed.")
            msg = "One or more ingestion tasks failed. Check logs for details."
            raise Exception(msg)

        logger.info("All ingestion tasks completed.")
