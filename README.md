# Retirement Planner

This project provides a simple Streamlit application for experimenting with retirement scenarios. It lets you explore how regular contributions, lump sums, market growth and inflation impact your portfolio over time. The app displays the projected growth of your investments and your progress toward a retirement fund goal.

## Current Features

- Monthly compounding of investment returns
- Inflation-adjusted projections
- Flexible inputs for age, fund target, contributions, lump sums and withdrawals
- Charts comparing contributions with portfolio value
- Download buttons for the underlying data and generated charts

## Requirements

- Python 3.7+
- `streamlit`
- `pandas`
- `matplotlib`

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Running the App

Clone the repository and launch the Streamlit application:

```bash
git clone https://github.com/YOUR_USERNAME/retirement-planner.git
cd retirement-planner
pip install -r requirements.txt
streamlit run retirement_planner.py
```

