"""Interactive Streamlit app to explore retirement scenarios."""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta


def calculate_retirement_plan(
    current_age,
    retirement_age,
    target_fund,
    annual_growth,
    annual_inflation,
    monthly_contribution,
    monthly_withdrawal,
    lump_sums,
    years,
    inflation_adjusted_withdrawals,
):
    """Return a projection of portfolio value over time.

    Parameters are expressed in annual percentages and monthly dollar amounts.
    ``lump_sums`` is a mapping of month indexes to contribution amounts.
    The resulting ``DataFrame`` contains monthly values and progress toward the
    savings goal or retirement age.
    """

    # Convert year-based inputs to monthly units
    months = years * 12
    current_month = 0
    age = current_age
    balance = 0
    monthly_rate = annual_growth / 12 / 100
    monthly_inflation = annual_inflation / 12 / 100

    # Tracking containers for the simulation
    balances = []
    real_balances = []
    cumulative_contributions = []
    withdrawals = []
    goal_progress = []
    inflation_multiplier = 1.0
    contribution_total = 0

    # Determine target and retirement month in terms of months
    target_balance = target_fund if target_fund > 0 else None
    retirement_month = (retirement_age - current_age) * 12 if retirement_age else None

    # Run the month-by-month simulation
    for month in range(months + 1):
        # Add any lump sum contributions for this month
        if month in lump_sums:
            balance += lump_sums[month]
            contribution_total += lump_sums[month]

        # Add regular contributions while still employed
        if retirement_month is None or month < retirement_month:
            balance += monthly_contribution
            contribution_total += monthly_contribution
        else:
            # Withdraw from the portfolio after retirement
            withdrawal = (
                monthly_withdrawal * inflation_multiplier
                if inflation_adjusted_withdrawals
                else monthly_withdrawal
            )
            balance -= withdrawal
            withdrawals.append(withdrawal)
        # Apply monthly growth and track results
        balance *= 1 + monthly_rate
        balances.append(balance)
        real_balances.append(balance / inflation_multiplier)
        cumulative_contributions.append(contribution_total)
        goal_progress.append(balance >= target_fund if target_fund else month >= retirement_month)
        inflation_multiplier *= 1 + monthly_inflation

    # Collect the results into a DataFrame for easy use in the UI
    df = pd.DataFrame({
        "Month": list(range(months + 1)),
        "Age": [current_age + m // 12 for m in range(months + 1)],
        "Total Value": balances,
        "Inflation-Adjusted Value": real_balances,
        "Cumulative Contributions": cumulative_contributions,
        "Reached Goal": goal_progress,
    })
    return df


def plot_growth(df):
    """Return a matplotlib figure showing portfolio growth."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Month"], df["Total Value"], label="Total Value")
    ax.plot(
        df["Month"],
        df["Inflation-Adjusted Value"],
        label="Inflation-Adjusted Value",
        linestyle="--",
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Value ($)")
    ax.set_title("Investment Growth Over Time")
    ax.legend()
    ax.grid(True)
    return fig


def plot_progress_vs_contribution(df):
    """Return a figure comparing contributions with portfolio value."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Month"], df["Cumulative Contributions"], label="Contributions", linestyle="--")
    ax.plot(df["Month"], df["Total Value"], label="Total Value")
    ax.set_xlabel("Month")
    ax.set_ylabel("Value ($)")
    ax.set_title("Contributions vs Portfolio Value")
    ax.legend()
    ax.grid(True)
    return fig


def convert_df_to_csv(df):
    """Encode the dataframe as CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")


def convert_plot_to_png(fig):
    """Serialize a matplotlib figure to PNG bytes."""
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf


def main():
    """Streamlit app entry point."""
    st.title("Retirement Planner")

    # --- Input section ---
    # Collect basic configuration from the user
    col1, col2 = st.columns(2)
    with col1:
        current_age = st.number_input("Your Current Age", min_value=18, max_value=100, value=35)
        retirement_age = st.number_input("Retirement Age (optional)", min_value=18, max_value=100, value=65)
        target_fund = st.number_input("Target Retirement Fund ($, optional)", min_value=0.0, value=1_000_000.0)
    with col2:
        annual_growth = st.number_input("Expected Annual Growth (%)", min_value=0.0, value=7.0)
        annual_inflation = st.number_input("Expected Annual Inflation (%)", min_value=0.0, value=2.5)
        years = st.slider("Years to Simulate", min_value=1, max_value=70, value=50)

    monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, value=1000.0)
    monthly_withdrawal = st.number_input("Monthly Withdrawal After Retirement ($)", min_value=0.0, value=4000.0)
    inflation_adjusted_withdrawals = st.checkbox("Inflation-adjusted withdrawals?", value=True)

    # Parse any optional lump sum contributions
    lump_years = st.text_input(
        "Years and Amounts (format: year1:amount1, year2:amount2)",
        value="5:20000, 10:30000",
    )
    lump_sums = {}
    try:
        for pair in lump_years.split(","):
            if ":" in pair:
                y, a = pair.split(":")
                lump_sums[int(y.strip()) * 12] = float(a.strip())
    except Exception:
        st.warning("Invalid lump sum format. Use format like '5:20000, 10:30000'")

    # --- Perform calculation when the user presses the button ---
    if st.button("Calculate Retirement Plan"):
        df = calculate_retirement_plan(
            current_age=current_age,
            retirement_age=retirement_age,
            target_fund=target_fund,
            annual_growth=annual_growth,
            annual_inflation=annual_inflation,
            monthly_contribution=monthly_contribution,
            monthly_withdrawal=monthly_withdrawal,
            lump_sums=lump_sums,
            years=years,
            inflation_adjusted_withdrawals=inflation_adjusted_withdrawals,
        )

        # Display when the savings goal will be reached (if provided)
        st.subheader("Progress Toward Retirement Goal")
        if target_fund > 0:
            reached = df[df["Reached Goal"]]
            if not reached.empty:
                first_hit = reached.iloc[0]
                months_to_goal = int(first_hit["Month"])
                projected_date = datetime.today() + timedelta(days=months_to_goal * 30)
                st.success(
                    f"Goal of ${target_fund:,.0f} will be reached in {months_to_goal // 12} years and {months_to_goal % 12} months."
                )
                st.write(f"Projected date: **{projected_date.strftime('%B %Y')}**")
            else:
                st.warning("Goal not reached in the given timeframe.")
        else:
            st.info(f"Plan simulates retirement at age {retirement_age}.")

        # Generate and display charts
        fig1 = plot_growth(df)
        st.pyplot(fig1)

        fig2 = plot_progress_vs_contribution(df)
        st.pyplot(fig2)

        # Provide downloads of the data and charts
        st.download_button(
            "Download Data as CSV",
            convert_df_to_csv(df),
            "retirement_data.csv",
            "text/csv",
        )
        st.download_button(
            "Download Growth Chart",
            convert_plot_to_png(fig1),
            "retirement_growth.png",
            "image/png",
        )
        st.download_button(
            "Download Progress Chart",
            convert_plot_to_png(fig2),
            "contribution_vs_value.png",
            "image/png",
        )


if __name__ == "__main__":
    main()
