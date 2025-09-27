from  .deltalake_tables import (
    FactDailyResult as FactDailyResultDeltaLake,
)
from .spark_tables import (
    FactDailyResult as FactDailyResultSpark,
)

__all__ = [
    "FactDailyResultDeltaLake",
    "FactDailyResultSpark",
]