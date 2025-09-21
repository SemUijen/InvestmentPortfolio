# Investment ETL Pipeline 📊

A robust, medallion architecture-based ETL pipeline for investment portfolio data processing using PySpark, Delta Lake, and Apache Spark. This pipeline extracts financial data from external APIs, processes it through Bronze → Silver → Gold layers, and creates analytics-ready datasets for investment portfolio analysis.

## 🏗️ Architecture Overview

The Investment ETL follows the **Medallion Architecture** pattern with three distinct layers:

```
  🥉 BRONZE         🥈 SILVER            🥇 GOLD
  (Raw Data) ───▶ (Cleaned Data) ───▶ (Business Ready)
```

### Bronze Layer (Raw Data Ingestion)

- **Purpose**: Raw data ingestion from external APIs
- **Data Sources**: AlphaVantage API for stock prices and currency exchange rates
- **Storage Format**: JSON files partitioned by date
- **Key Features**:
  - Asynchronous data fetching with rate limiting
  - Automatic file organization by year/month/day
  - Support for both full and incremental data loads

### Silver Layer (Data Cleaning & Validation)

- **Purpose**: Clean, validate, and standardize raw data
- **Storage Format**: Delta Lake tables
- **Key Features**:
  - Schema enforcement and validation
  - Data quality checks and transformations
  - Historical data preservation with SCD Type 2
  - Weekend gap filling for financial markets

### Gold Layer (Business Intelligence)

- **Purpose**: Create aggregated, business-ready datasets
- **Storage Format**: Delta Lake fact and dimension tables
- **Key Features**:
  - Star/snowflake schema implementation
  - Daily portfolio performance calculations
  - Currency conversion and profit/loss analysis

## 📁 Project Structure

```
investment_etl/
├── investment_etl/
│   ├── app.py                    # Main pipeline orchestrator
│   ├── bronze_layer/             # Raw data ingestion
│   │   ├── app.py               # Bronze layer main entry point
│   │   ├── stockprobe/          # API integration modules
│   │   │   └── alphavantage/    # AlphaVantage API client
│   │   │       └── url_generator/
│   │   └── utils/
│   │       └── async_data_ingestor.py  # Async data fetching
│   ├── silver_layer/            # Data cleaning and validation
│   │   ├── app.py              # Silver layer main entry point
│   │   ├── tables/             # Table definitions
│   │   │   ├── spark_tables/   # Spark-based table schemas
│   │   │   └── deltalake_tables/  # Delta Lake table implementations
│   │   └── utils/
│   │       ├── bronze_source.py      # Bronze data reader
│   │       ├── silver_pipeline.py    # Processing pipeline
│   │       └── transformations/      # Data transformation functions
│   ├── gold_layer/              # Business intelligence layer
│   │   ├── app.py              # Gold layer main entry point
│   │   ├── tables/             # Fact and dimension tables
│   │   │   ├── fact/           # Fact tables (daily results)
│   │   │   └── dimensions/     # Dimension tables (date, etc.)
│   │   └── pipelines/
│   │       └── enrich_daily_results.py  # Daily aggregation pipeline
│   └── utils/                   # Shared utilities
│       ├── spark_session/       # Spark configuration
│       └── spark_tables/        # Base table classes
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## 📊 Data Flow & Processing

### 1. Bronze Layer Processing

```python
# The bronze layer fetches:
# - Daily stock prices for all investment options
# - Currency exchange rates (USD/EUR)
```

**Output Format**:

```
bronze/
├── investment_options/
│   └── AAPL/
│       └── year=2024/month=09/day=21/
│           └── 2024-09-21_AAPL.json
└── exchange_rate/
    └── USD_EUR/
        └── year=2024/month=09/day=21/
            └── 2024-09-21_USD_EUR.json
```

### 2. Silver Layer Processing

**Key Tables**:

- `investment_option_value_overtime`: Daily stock prices with filled weekends
- `currency_exchange_rate`: Daily USD/EUR exchange rates
- `investment_option_bought`: Portfolio purchase history
- `io_stock_exchange`: Symbol mappings between internal and exchange symbols

### 3. Gold Layer Processing

**Key Tables**:

- `fact_daily_result`: Daily portfolio performance metrics
- `dim_date`: Date dimension for time-series analysis

## 🔧 Advanced Configuration

### Spark Configuration

The pipeline uses PySpark with Delta Lake. Key configurations:

```python
# Automatic Spark session creation with Delta Lake support
from investment_etl.utils import get_spark_session

spark = get_spark_session()
# Pre-configured with:
# - Delta Lake extensions
# - Optimized for local development
# - Memory and disk configurations
```

## 🤝 Contributing

Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines, coding standards, and contribution processes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
