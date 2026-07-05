#!/usr/bin/env bash
export PYTHONPATH="/home/sem_uijen/repos/InvestmentPortfolio/investment_gui"
cd "/home/sem_uijen/repos/InvestmentPortfolio/investment_gui"
"/home/sem_uijen/repos/InvestmentPortfolio/investment_gui/.venv/bin/python" "/home/sem_uijen/repos/InvestmentPortfolio/investment_gui/investment_gui/app.py"
status=$?
if [ $status -ne 0 ]; then
  echo ""
  echo "App exited with status $status. Press Enter to close."
  read
fi
