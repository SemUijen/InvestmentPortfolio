"""Run full medaillon pipeline."""

import asyncio

from .bronze_layer import app as bronze_pipelines
from .gold_layer import app as gold_pipelines
from .silver_layer import app as silver_pipelines


async def main() -> None:
    """Run full medaillon pipeline."""
    await bronze_pipelines.main()
    silver_pipelines.main()
    gold_pipelines.main()


if __name__ == "__main__":
    asyncio.run(main())
