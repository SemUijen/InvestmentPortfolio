# Investment Portfolio GUI

A desktop GUI application for managing investment portfolio data and running ETL pipelines. Built with Python Tkinter and integrated with Docker containerization for seamless pipeline execution.

## 🎯 Overview

The Investment GUI provides a user-friendly interface to:

- Add and manage investment options (stocks, ETFs, etc.)
- Record portfolio purchases and transactions
- Execute the medallion ETL pipeline via Docker
- Create desktop shortcuts for easy access

## 🖥️ Application Screens

### 📱 Main Navigation (Startup Screen)

The main menu provides access to all application features:

### 📊 Investment Options Screen

Add new investment instruments to track:

**Features:**

- **Symbol Validation**: Real-time validation against AlphaVantage API
- **Stock Exchange Integration**: Automatic exchange detection and mapping
- **Search Functionality**: Symbol lookup with company information
- **Data Persistence**: Saves to Delta Lake tables for ETL processing

**Workflow:**

1. Enter stock symbol (e.g., "AAPL", "VWCE.DE")
2. System validates symbol via AlphaVantage API
3. Retrieves Stock information and exchange details
4. Saves validated data to investment tables

### 💰 Portfolio Management Screen

Record investment purchases and transactions:

**Data Capture:**

- **Investment Symbol**: From validated investment options
- **Purchase Date**: Date of transaction
- **Quantity**: Number of shares/units purchased
- **Price Paid**: Purchase price per unit
- **Currency**: Transaction currency (USD/EUR)

**Features:**

- **Date Validation**: Ensures realistic transaction dates
- **Currency Support**: Multi-currency transaction recording
- **Decimal Precision**: Accurate financial calculations
- **Data Integrity**: Validates against existing investment options

### 🐳 Docker Pipeline Integration

Execute ETL pipelines directly from the GUI:

**Pipeline Execution:**

- One-click pipeline execution via Docker Compose
- Real-time execution status and feedback
- Error handling with detailed error messages
- Background processing with progress indicators

## 🏗️ Application Architecture

### 📁 Project Structure

```
investment_gui/
├── investment_gui/
│   ├── app.py                    # Application entry point
│   └── application/
│       ├── application.py        # Main app controller
│       └── screens/
│           ├── base_screen.py    # Base screen class
│           ├── start_screen.py   # Navigation menu
│           ├── add_investment_option_screen.py
│           └── add_bought_io_screen.py
├── docker/
│   ├── docker-compose.yml       # Pipeline orchestration
│   └── run_medaillon/
│       ├── Dockerfile           # ETL container definition
│       └── requirements.txt     # Pipeline dependencies
├── create_desktop_shortcut.py   # Desktop shortcut creator
└── InvestmentPortfolio.bat     # Windows launcher script
```

### 🎨 GUI Framework Architecture

## 🐳 Docker Integration

### 📦 Container Architecture

The GUI integrates with a containerized ETL pipeline for seamless data processing:

**Docker Compose Configuration:**

```yaml
services:
  run-medaillon-pipeline:
    container_name: run-medaillon-pipeline
    build:
      context: ./run_medaillon
      dockerfile: ./Dockerfile
    volumes:
      - E:/InvestmentPortfolioData:/mnt/data
    environment:
      DATA_DIR: "/mnt/data"
```

**Container Features:**

- **Spark 4.0 Runtime**: Full Apache Spark environment
- **Python 3.12**: Latest Python with optimized performance
- **Delta Lake Support**: ACID transactions and data versioning
- **Volume Mounting**: Persistent data storage outside container
- **Environment Isolation**: Clean, reproducible execution environment

### 🔄 Pipeline Execution Flow

```
GUI Button Click
    │
    ├── Docker Compose Command
    │   └── docker-compose run --rm run-medaillon-pipeline
    │
    ├── Container Startup
    │   ├── Mount data volumes
    │   ├── Load environment variables
    │   └── Initialize Spark session
    │
    ├── ETL Pipeline Execution
    │   ├── Bronze Layer: Data ingestion
    │   ├── Silver Layer: Data cleaning
    │   └── Gold Layer: Business logic
    │
    └── Status Feedback
        ├── Success: "Pipeline completed successfully!"
        └── Error: Detailed error message with troubleshooting
```

## 🖱️ Desktop Integration

### 🔗 Desktop Shortcut Creation

The application includes automated desktop shortcut creation:

**Features:**

- **Windows Integration**: Native .bat file and .lnk shortcut creation
- **Custom Icon**: Professional currency icon for easy recognition
- **Path Resolution**: Automatic virtual environment detection
- **One-Click Setup**: Single script execution for complete setup

**Shortcut Creation Process:**

```python
def create_bat_shortcut():
    # 1. Create .bat launcher file
    # 2. Generate Windows shortcut (.lnk)
    # 3. Set custom icon and metadata
    # 4. Place on desktop for easy access
```

**Generated Files:**

- InvestmentPortfolio.bat: Command-line launcher
- Desktop shortcut with custom icon
- Start menu integration (optional)
