# 💰 Investment Portfolio Management System

A comprehensive, end-to-end investment portfolio management and analytics platform built with modern data engineering practices. The system combines real-time data ingestion, advanced analytics, and interactive visualizations to provide complete investment portfolio insights.

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [�️ Prerequisites](#️-prerequisites)
- [🚀 Installation & Setup](#-installation--setup)
- [⚡ Quick Start Guide](#-quick-start-guide)
- [💡 Usage Examples](#-usage-examples)
- [📁 Project Structure](#-project-structure)
- [🔧 Component Overview](#-component-overview)
- [⚙️ Configuration](#️-configuration)

## 🛠️ Prerequisites

### 📋 **System Requirements**

- **Operating System**: Windows 10/11
- **Python**: 3.12 or higher
- **Java**: JDK 8 or 11 (required for Apache Spark)

### 🔑 **Required Services**

- **AlphaVantage API**: Free tier provides 25 requests/day, 5 requests/minute
  - Sign up at: https://www.alphavantage.co/support/#api-key
- **Docker (Desktop)**: For containerized ETL execution
- **PowerBI Desktop**: For dashboard visualization (Windows only)
- **uv**: Fast Python package manager (recommended over pip)
  - https://docs.astral.sh/uv/getting-started/installation/

### 📦 **Development Tools**

- **Git**: Version control for code management
- **VS Code**: Development environment extensions
  - **mypy**: Static type checker for Python
  - **ruff**: Fast Python linter and formatter

## 🚀 Installation & Setup

### 1️⃣ **Clone Repository**

```bash
git clone https://github.com/SemUijen/InvestmentPortfolio.git
cd InvestmentPortfolio
```

### 2️⃣ **ETL Pipeline Setup**

```bash
cd investment_etl

# Install dependencies (recommended: use uv)
uv sync

# Alternative: using pip
pip install -e .
```

### 3️⃣ **GUI Application Setup**

```bash
cd ../investment_gui

# Install GUI dependencies
uv sync

# Create desktop shortcut (Windows only)
python create_desktop_shortcut.py
```

### 4️⃣ **Environment Configuration**

Create `.env` files in both `investment_etl/` and `investment_gui/docker/run_medaillon/`:

```env
# AlphaVantage API Configuration
ALPHAVANTAGE_API_KEY=your_api_key_here

# Data Storage Configuration
DATA_DIR=/path/to/your/data/directory
```

### 5️⃣ **Docker Setup**

```bash
# Install Docker Desktop from: https://docker.com/desktop

# Build ETL container
cd investment_gui/docker
docker-compose build
```

### 6️⃣ **PowerBI Setup**

1. Install PowerBI Desktop from Microsoft Store
2. Open `powerbi/InvestmentPortfolioDashboard.pbip`
3. Update data source paths to match your `DATA_DIR`
4. Refresh data connections

## ⚡ Quick Start Guide

### **Step 1: Launch GUI Application**

1. Go to Add Investment Options
2. Add an existing investments options (E.G. AAPL, MSFT, VWCE etc.)
3. Go to Data Input
4. Select the investment option you just added
5. Input the transaction details (date, quantity, price, fees, etc.)
6. Run the ETL pipeline to process and store data

### **Step 2: Open PowerBI Dashboard**

1. Launch PowerBI Desktop
2. Open the `InvestmentPortfolioDashboard.pbip` file
3. Update the data source paths to match your `DATA_DIR`
4. Refresh the data connections

#### **PowerBI Configuration**

- **Data Source Path**: Update in PowerBI Desktop to match your `DATA_DIR`
- **Refresh Schedule**: Configure automatic refresh in PowerBI Service
- **Currency Display**: Defaults to EUR, customizable in measures

## 📁 Project Structure

```
InvestmentPortfolio/
├── README.md                           # Main project documentation
├──
├── investment_etl/                     # ETL Pipeline (Medallion Architecture)
│   ├── README.md                       # ETL-specific documentation
│   ├── ARCHITECTURE.md                 # Technical architecture diagrams
│   ├── pyproject.toml                  # ETL dependencies and configuration
│   ├── uv.lock                         # Dependency lock file
│   ├── mypy.ini                        # Type checking configuration
│   ├── ruff.toml                       # Code formatting and linting
│   └── investment_etl/
│       ├── app.py                      # Main ETL orchestrator
│       ├── bronze_layer/               # Raw data ingestion
│       │   ├── app.py                  # Bronze layer entry point
│       │   ├── stockprobe/             # AlphaVantage API integration
│       │   │   └── alphavantage/       # API client and URL generators
│       │   └── utils/                  # Async data ingestor utilities
│       ├── silver_layer/               # Data cleaning and validation
│       │   ├── app.py                  # Silver layer entry point
│       │   ├── tables/                 # Delta Lake table definitions
│       │   │   ├── spark_tables/       # Spark-based table management
│       │   │   └── deltalake_tables/   # Native Delta Lake operations
│       │   └── utils/                  # Data transformation utilities
│       ├── gold_layer/                 # Business intelligence
│       │   ├── app.py                  # Gold layer entry point
│       │   ├── pipelines/              # Business logic pipelines
│       │   └── tables/                 # Fact and dimension tables
│       └── utils/                      # Shared utilities
│           ├── spark_session/          # Spark configuration
│           └── spark_tables/           # Base table classes
│
├── investment_gui/                     # Desktop GUI Application
│   ├── README.md                       # GUI-specific documentation
│   ├── pyproject.toml                  # GUI dependencies
│   ├── create_desktop_shortcut.py      # Desktop integration utility
│   ├── InvestmentPortfolio.bat         # Windows launcher script
│   ├── currency.ico                    # Application icon
│   ├── investment_gui/
│   │   ├── app.py                      # GUI application entry point
│   │   └── application/
│   │       ├── application.py          # Main application controller
│   │       └── screens/                # GUI screen components
│   │           ├── base_screen.py      # Base screen class
│   │           ├── start_screen.py     # Main navigation screen
│   │           ├── add_investment_option_screen.py
│   │           └── add_bought_io_screen.py
│   └── docker/                         # Docker containerization
│       ├── docker-compose.yml          # Container orchestration
│       └── run_medaillon/              # ETL container definition
│           ├── Dockerfile              # Container image specification
│           └── requirements.txt        # Container dependencies
│
├── powerbi/                           # Business Intelligence Dashboard
│   ├── README.md                      # PowerBI documentation
│   ├── InvestmentPortfolioDashboard.pbip  # PowerBI project file
│   ├── InvestmentPortfolioDashboard.Report/     # Report definitions
│   │   ├── definition.pbir            # Report configuration
│   │   └── definition/                # Page and visualization definitions
│   │       ├── report.json            # Main report structure
│   │       └── pages/                 # Individual dashboard pages
│   └── InvestmentPortfolioDashboard.SemanticModel/  # Data model
│       ├── definition.pbism           # Semantic model configuration
│       ├── diagramLayout.json         # Visual relationship diagram
│       └── definition/                # Model definitions
│           ├── model.tmdl             # Core data model
│           ├── relationships.tmdl     # Table relationships
│           └── tables/                # Table definitions with DAX measures
│
└── .gitignore                         # Version control exclusions
```

## 🔧 Component Overview

### 🏭 **ETL Pipeline** (`investment_etl/`)

**Purpose**: Data ingestion, processing, and storage using medallion architecture

**Key Features**:

- **Bronze Layer**: Raw JSON data from AlphaVantage API
- **Silver Layer**: Cleaned, validated Delta Lake tables
- **Gold Layer**: Business-ready fact tables for analytics
- **Async Processing**: Rate-limited API calls with error handling

[📖 **Detailed Documentation**](investment_etl/README.md) | [🏗️ **Architecture Diagrams**](investment_etl/ARCHITECTURE.md)

### 🖥️ **GUI Application** (`investment_gui/`)

**Purpose**: User-friendly desktop interface for portfolio management

**Key Features**:

- **Portfolio Management**: Add investments and record transactions
- **API Integration**: Real-time stock symbol validation
- **Docker Integration**: One-click ETL pipeline execution
- **Desktop Shortcuts**: Native Windows application experience

[📖 **Detailed Documentation**](investment_gui/README.md)

### 📊 **PowerBI Dashboard** (`powerbi/`)

**Purpose**: Advanced analytics and visualization platform

**Key Reports**:

- **Performance Tracking**: Real-time portfolio valuation and profit/loss

[📖 **Detailed Documentation**](powerbi/README.md)


