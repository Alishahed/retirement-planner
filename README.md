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

After running the command, a new browser window should open displaying the interactive retirement planner.

## Disclaimer

This project is a learning tool and does not constitute financial advice. Always consult with a qualified professional when making investment decisions.

## Proposals for Improvement

Below are ideas for extending the project:

- **User accounts and persistence**: store user scenarios so they can be revisited later.
- **Monte Carlo simulation** for returns to illustrate risk and uncertainty.
- **CSV import/export** for lump sum contributions and withdrawals.
- **Unit tests** for the calculation functions to ensure accuracy.
- **Performance optimizations** such as vectorizing calculations with NumPy.
- **Responsive layout** improvements for mobile devices.

Contributions and suggestions are welcome!

