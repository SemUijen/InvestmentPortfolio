# Contributing to Investment Portfolio Management System

Thank you for your interest in contributing to the Investment Portfolio Management System! This guide will help you get started with contributing to this comprehensive data-driven investment analytics platform.

## 📋 Table of Contents

- [🎯 Ways to Contribute](#-ways-to-contribute)
- [🚀 Getting Started](#-getting-started)
- [🏗️ Development Environment Setup](#️-development-environment-setup)
- [📝 Coding Standards](#-coding-standards)
- [🧪 Testing Guidelines](#-testing-guidelines)

## 🎯 Ways to Contribute

We welcome contributions in various forms:

### 🔧 **Code Contributions**

- **ETL Pipeline Enhancements**: Improve data processing, add new data sources, optimize performance
- **GUI Features**: Enhance user interface, add new screens, improve user experience
- **PowerBI Analytics**: Create new dashboards, add advanced visualizations, develop custom measures
- **Infrastructure**: Improve Docker configurations, optimize Spark settings, enhance deployment

## 🚀 Getting Started

### 1️⃣ **Fork and Clone**

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/InvestmentPortfolio.git
cd InvestmentPortfolio

# Add upstream remote
git remote add upstream https://github.com/SemUijen/InvestmentPortfolio.git
```

### 2️⃣ **Choose Your Contribution Area**

- **ETL Development**: Focus on `investment_etl/` directory
- **GUI Development**: Focus on `investment_gui/` directory
- **Analytics Development**: Focus on `powerbi/` directory
- **Full-Stack**: Work across multiple components

## 📝 Coding Standards

### 🐍 **Python Code Style**

#### **Code Formatting**

We use **Ruff** for code formatting and linting:

```bash
# Format code
ruff format investment_etl/ investment_gui/

# Check for linting issues
ruff check investment_etl/ investment_gui/

# Auto-fix issues where possible
ruff check --fix investment_etl/ investment_gui/
```

#### **Type Hints**

All new code must include comprehensive type hints:

```python
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime

def calculate_portfolio_value(
    investments: Dict[str, Decimal],
    prices: Dict[str, Decimal],
    currency_rate: Optional[Decimal] = None
) -> Decimal:
    total_value = Decimal('0')
    for symbol, quantity in investments.items():
        if symbol not in prices:
            raise ValueError(f"Price data missing for symbol: {symbol}")
        total_value += quantity * prices[symbol]

    if currency_rate:
        total_value *= currency_rate

    return total_value
```

### 📊 **Test Coverage Requirements**

- **New Code**: Minimum 90% test coverage
- **Bug Fixes**: Must include regression tests
- **Critical Path**: 100% coverage for core financial calculations
- **Integration Points**: Full coverage of component interfaces

## 📝 **Documentation Standards**

#### **Code Documentation**

```python
def calculate_compound_interest(
    principal: Decimal,
    rate: Decimal,
    time: int,
    frequency: int = 1
) -> Decimal:
    """Calculate compound interest for investment.

    Uses the compound interest formula: A = P(1 + r/n)^(nt)
    where A is final amount, P is principal, r is annual rate,
    n is compounding frequency, and t is time in years.

    Args:
        principal: Initial investment amount
        rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
        time: Investment time period in years
        frequency: Compounding frequency per year (default: 1)

    Returns:
        Final investment amount after compound interest

    Raises:
        ValueError: If principal is negative or rate is invalid

    Example:
        >>> calculate_compound_interest(Decimal('1000'), Decimal('0.05'), 5)
        Decimal('1276.28')
    """
```

### 🎛️ **Contribution Options**

#### **ETL Pipeline Customization**

- **Data Sources**: Add new APIs by extending the `stockprobe` module
- **Transformations**: Custom business logic in silver layer transformations
- **Storage Formats**: Modify table schemas in the `tables/` directories
- **Scheduling**: Integrate with cron/Windows Task Scheduler for automation

#### **GUI**

- **Support for MacOS/Linux**: Ensure cross-platform compatibility by implementing differnt gui
- **Themes**: Modify tkinter theme settings in `application.py`
- **Screen Layouts**: Add new screens by extending `BaseScreen` class
- **Validation Rules**: Customize input validation in screen components
- **Integration**: Add new external service integrations

#### **PowerBI Customization**

- **Visualizations**: Add custom charts and KPI cards
- **Measures**: Create new DAX measures for specific metrics
- **Pages**: Design additional dashboard pages for specific analysis
- **Themes**: Apply custom color schemes and branding
