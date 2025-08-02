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
            logging.info("Status %s", response.status)
            response.raise_for_status()  # Raise an error for bad responses
            return await response.json()

    async def save_data(self, data: dict, file_path: str) -> None:
        """Save the fetched data to a file."""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, "w") as file:
            await file.write(json.dumps(data, indent=4))
            logging.info("Data saved to %s", file_path)

    async def ingest(self, url: str, symbol_name: str) -> None:
        """Ingest data from the URL and save it to a file."""
        try:
            logging.info("Starting data ingestion for %s", symbol_name)
            data = await self.fetch_data(url=url)
            file_path = await self.create_file_path(symbol_name)
            await self.save_data(data, file_path)
            logging.info("Data ingestion completed successfully.")
        except Exception as e:
            logging.exception("Error during data ingestion: %s", e)
            raise

    async def create_file_path(self, symbol_name: str) -> str:
        """Create a file path for saving data."""
        today = date.today()
        symbol_name = symbol_name.split(".")[0]  # Remove exchange suffix if present
        file_name = f"{today}_{symbol_name}.json"
        directory = (
            Path(self.base_dir)
            / symbol_name
            / f"year={today.year}"
            / f"month={today.month}"
            / f"day={today.day}"
        )
        return rf"{directory}\{file_name}"

    async def ingest_all(self) -> None:
        """Ingest data from all URLs concurrently."""
        tasks = []
        for url, symbol_name in self.to_ingest:
            task = self.ingest(url, symbol_name)
            tasks.append(task)

        # Execute all tasks concurrently
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("All ingestion tasks completed.")
