import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier, risk_models, expected_returns, plotting
from datetime import datetime
from pypfopt.objective_functions import L2_reg

from PortfolioUtils import load_and_prepare_data, rebalance_portfolio, calculate_cumulative_returns, calculate_metrics
from OptContentManager import OptContent
from SimContentManager import SimContent

# Set the page configuration
st.set_page_config(
    page_title="Portfolio Management Toolkit",  # Title of the web page
    page_icon="💰",  # Emoji or icon
    layout="centered",  # Can be "centered" or "wide"
    initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
)

# Streamlit app title
st.title("Portfolio Management Toolkit")

# Sidebar navigation
header = st.sidebar.title("⚙️ Settings")
divider = st.sidebar.divider()
page = st.sidebar.selectbox("Select Portfolio Tool", ["Optimizer", "Simulator"], help= "Select the portfolio tool youd like to use")
# Common inputs
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2000-01-01"), help="Select the start date for the analysis")
end_date = st.sidebar.date_input("End Date", value=pd.Timestamp.now(),  help="Select the end date for the analysis")
initial_value = st.sidebar.number_input("Initial Portfolio Value", value=10000, help="This will be the initial investment value for all analysis")
benchmark = st.sidebar.selectbox("Select Benchmark", [
    "SPY (S&P 500 ETF - Tracks the performance of the S&P 500 Index)",
    "DIA (Dow Jones Industrial Average ETF - Tracks the performance of 30 large publicly-owned companies in the U.S.)",
    "QQQ (NASDAQ-100 ETF - Tracks the performance of the 100 largest non-financial companies listed on the NASDAQ)",
    "IWM (Russell 2000 ETF - Tracks the performance of the 2000 smallest stocks in the Russell 3000 Index)",
    "VTI (Vanguard Total Stock Market ETF - Tracks the performance of the entire U.S. stock market)"
], help="This is what we will be comparing our portfolio to. To get an idea of how good were doing compared to common investments")
benchmark_ticker = benchmark.split(" ")[0]

if page ==  "Optimizer":
    # efficient frontier page content
    st.write("""
    ## 🎯 Optimize Your Investment Portfolio

    Use this tool to find the best way to balance your investments using advanced methods such as mean-variance optimization and regularization techniques. Whether you aim for maximum returns or minimum risk, this tool helps you create a portfolio that suits your goals.
    """)

    with st.expander("❓ How to Use This Tool"):
        st.write(OptContent.howToUse())

    with st.expander("💡 Insights"):
        st.write(OptContent.importantDefinitions())

    with st.expander("📝 Example Walkthrough"):
        st.write(OptContent.exampleWalkthrough())

    #split ticker names into a list
    tickers_input = st.text_input("Enter tickers:", "SPY,TLT,TSLA,TLT,GLD,GOOGL,DBC")
    tickers = [ticker.strip() for ticker in tickers_input.split(",")]



    # button to add L2 regularization
    l2_reg = st.checkbox("L2 Regularization")
    if l2_reg:
        st.write("""
        [L2 Regularization](https://en.wikipedia.org/wiki/Ridge_regression) has been enabled. This promotes diversification by penalizing large weights in the portfolio. 
        """)


    if st.button("Optimize Portfolio"):
        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        benchmark_data = yf.download(benchmark_ticker, start=start_date, end=end_date)['Adj Close']

        # align dates
        common_dates = data.dropna().index.intersection(benchmark_data.dropna().index)
        data = data.loc[common_dates]
        benchmark_data = benchmark_data.loc[common_dates]

        # calculating expected returns and covariance matrix using Ledoit-Wolf Shrinkage Method
        mu = expected_returns.mean_historical_return(data)
        S = risk_models.CovarianceShrinkage(data).ledoit_wolf()

        # run optimization and plot it
        ef = EfficientFrontier(mu, S)

        # Conditionally add L2 regularization
        if l2_reg:
            ef.add_objective(L2_reg)

        fig, ax = plt.subplots(figsize=(12, 8))
        plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True, show_tickers=True)
        plt.title("Efficient Frontier", fontsize=25)
        plt.xlabel("Risk (Standard Deviation)", fontsize=17)
        plt.ylabel("Expected Return", fontsize=17)
        plt.grid(True)
        plt.legend()

        for text in ax.texts:
            text.set_fontsize(14)

        ef_sharpe = EfficientFrontier(mu, S)
        if l2_reg:
            ef_sharpe.add_objective(L2_reg)
        ef_min_vol = EfficientFrontier(mu, S)
        if l2_reg:
            ef_min_vol.add_objective(L2_reg)

        # Show max sharpe portfolio
        ef_sharpe.max_sharpe()
        weights_sharpe = ef_sharpe.clean_weights()
        performance_sharpe = ef_sharpe.portfolio_performance(verbose=True)
        ret_sharpe, std_sharpe, _ = performance_sharpe
        ax.scatter(std_sharpe, ret_sharpe, marker="*", s=150, c="g", label="Max Sharpe")
        ax.annotate('Max Sharpe Weighting', xy=(std_sharpe, ret_sharpe), xytext=(std_sharpe + 0.005, ret_sharpe),
                    arrowprops=dict(facecolor='green', shrink=0.05), fontsize=20, color='green')

        # Show the min volatility portfolio only if target return is disabled (otherwise they'll be the same)
        ef_min_vol.min_volatility()
        weights_min_vol = ef_min_vol.clean_weights()
        performance_min_vol = ef_min_vol.portfolio_performance(verbose=True)
        ret_min_vol, std_min_vol, _ = performance_min_vol
        ax.scatter(std_min_vol, ret_min_vol, marker="*", s=150, c="b", label="Min Volatility")
        ax.annotate('Min Volatility Weighting', xy=(std_min_vol, ret_min_vol), xytext=(std_min_vol + 0.005, ret_min_vol),
                    arrowprops=dict(facecolor='blue', shrink=0.05), fontsize=20, color='blue')

        st.pyplot(fig)

        st.subheader("Maximum Sharpe Portfolio Metrics")
        st.write(f"**Expected annual return:** {performance_sharpe[0]*100:.2f}%")
        st.write(f"**Annual volatility:** {performance_sharpe[1]*100:.2f}%")
        st.write(f"**Sharpe Ratio:** {performance_sharpe[2]:.2f}")
        st.write("**Weightings of the Max Sharpe Portfolio:**")
        weights_sharpe_df = pd.DataFrame.from_dict(weights_sharpe, orient='index', columns=['Weight']).sort_values(by='Weight', ascending=False)
        weights_sharpe_df['Weight'] = weights_sharpe_df['Weight'] * 100
        weights_sharpe_df.columns = ['Weight (%)']
        st.dataframe(weights_sharpe_df)

        st.subheader("Minimum Volatility Portfolio Metrics")
        st.write(f"**Expected annual return:** {performance_min_vol[0]*100:.2f}%")
        st.write(f"**Annual volatility:** {performance_min_vol[1]*100:.2f}%")
        st.write(f"**Sharpe Ratio:** {performance_min_vol[2]:.2f}")
        st.write("**Weightings of the Minimum Volatility Portfolio:**")
        weights_min_vol_df = pd.DataFrame.from_dict(weights_min_vol, orient='index', columns=['Weight']).sort_values(by='Weight', ascending=False)
        weights_min_vol_df['Weight'] = weights_min_vol_df['Weight'] * 100
        weights_min_vol_df.columns = ['Weight (%)']
        st.dataframe(weights_min_vol_df)

        # Calculate benchmark performance
        benchmark_returns = benchmark_data.pct_change().dropna()
        benchmark_cumulative_returns = (1 + benchmark_returns).cumprod() * initial_value
        benchmark_performance = {
            "Expected annual return": benchmark_returns.mean() * 252,
            "Annual volatility": benchmark_returns.std() * np.sqrt(252),
            "Sharpe Ratio": (benchmark_returns.mean() * 252) / (benchmark_returns.std() * np.sqrt(252))
        }

        st.subheader(f"{benchmark_ticker} (Benchmark) Metrics")
        st.write(f"**Expected annual return:** {benchmark_performance['Expected annual return']*100:.2f}%")
        st.write(f"**Annual volatility:** {benchmark_performance['Annual volatility']*100:.2f}%")
        st.write(f"**Sharpe Ratio:** {benchmark_performance['Sharpe Ratio']:.2f}")

        st.write("""
        ### Performance of Portfolios
        Shows the backtested performance of the portfolios
        (NOTE: The start date is adjusted so all data is available at the time)
        """)

        cumulative_returns_sharpe = calculate_cumulative_returns(data, pd.Series(weights_sharpe), initial_value)
        cumulative_returns_min_vol = calculate_cumulative_returns(data, pd.Series(weights_min_vol), initial_value)
        cumulative_returns_benchmark = (1 + benchmark_data.pct_change().dropna()).cumprod() * initial_value

        fig, ax = plt.subplots(figsize=(12, 8))
        cumulative_returns_sharpe.plot(ax=ax, label='Max Sharpe Ratio Portfolio')
        cumulative_returns_min_vol.plot(ax=ax, label='Min Volatility Portfolio')
        cumulative_returns_benchmark.plot(ax=ax, label=f'{benchmark_ticker} (Benchmark)')
        plt.title(f"Performance of Portfolios ({start_date} to {end_date})", fontsize=18)
        plt.xlabel("Date", fontsize=14)
        plt.ylabel("Portfolio Value", fontsize=14)
        plt.legend()
        plt.grid(True)
        st.pyplot(fig)

        st.write("Tool Created by Alan")





elif page == "Simulator":
    st.write("""
    ## 📈 Test Your Investment Strategies

    Discover how your investment portfolio could behave using this simulation tool. Whether you want to test new ideas or analyze current investments, see the possibilities under various rebalancing scenarios.
    """)


    with st.expander("❓ How to Use This Tool"):
        st.write(SimContent.howToUse())

    with st.expander("💡 Insights You Will Gain"):
        st.write(SimContent.insights())

    # Example walkthroughs
    with st.expander("📝 Example Walkthrough 1: 60/40 Stock-Bond Split with Annual Rebalancing"):
        st.write(SimContent.exampleWalkthrough1())

    with st.expander("📝 Example Walkthrough 2: Testing the Ray Dalio All Weather Portfolio"):
        st.write(SimContent.exampleWalkthrough2())

    tickers_input = st.text_input("Enter comma-separated stock tickers (as per yahoo finance):", "SPY, AAPL, BTC-USD")
    tickers = [ticker.strip() for ticker in tickers_input.split(",")]
    weights_input = st.text_input("Enter comma-separated initial weights (must sum to 1 and match the number of tickers):", "0.33,0.33,0.34")
    weights = [float(weight.strip()) for weight in weights_input.split(",")]

    # Validate the input lengths
    if len(tickers) != len(weights):
        st.error("The number of tickers must match the number of weights.")
    else:
        rebalance_period = st.selectbox("Select Rebalance Period", ["annually", "semi-annually", "quarterly", "monthly", "none"])

        if st.button("Simulate Portfolio"):
            try:
                portfolio_history, benchmark_history, rebalance_dates = rebalance_portfolio(
                    tickers, benchmark_ticker, initial_value, weights, rebalance_period, start_date, end_date
                )

                st.write("### Portfolio Balance Over Time")
                fig, ax = plt.subplots(figsize=(12, 8))
                portfolio_history.plot(ax=ax, label='Portfolio')
                benchmark_history.plot(ax=ax, label=f'{benchmark_ticker} (Benchmark)')
                for i, rebalance_date in enumerate(rebalance_dates):
                    ax.axvline(x=rebalance_date, color='r', linestyle='--', lw=0.5)
                    if i == 0:  # Add label only for the first rebalance line
                        ax.axvline(x=rebalance_date, color='r', linestyle='--', lw=0.5, label='Rebalance')
                plt.title("Portfolio Balance Over Time", fontsize=18)
                plt.xlabel("Date", fontsize=14)
                plt.ylabel("Balance", fontsize=14)
                plt.legend()
                plt.grid(False)
                st.pyplot(fig)

                st.write("### Rebalance Dates")
                st.write(rebalance_dates)

                mean_return_portfolio, std_dev_portfolio, sharpe_ratio_portfolio = calculate_metrics(portfolio_history)
                mean_return_benchmark, std_dev_benchmark, sharpe_ratio_benchmark = calculate_metrics(benchmark_history)

                st.write("### Portfolio Performance Metrics")
                st.write(f"**Expected Annual Return:** {mean_return_portfolio * 100:.2f}%")
                st.write(f"**Annual Volatility (Standard Deviation):** {std_dev_portfolio * 100:.2f}%")
                st.write(f"**Sharpe Ratio:** {sharpe_ratio_portfolio:.2f}")

                st.write("### Benchmark Performance Metrics")
                st.write(f"**Expected Annual Return:** {mean_return_benchmark * 100:.2f}%")
                st.write(f"**Annual Volatility (Standard Deviation):** {std_dev_benchmark * 100:.2f}%")
                st.write(f"**Sharpe Ratio:** {sharpe_ratio_benchmark:.2f}")

                st.write("### Portfolio and Benchmark Ending Values")
                st.write(f"**Final Portfolio Balance:** ${portfolio_history.iloc[-1]:,.2f}")
                st.write(f"**Final Benchmark Balance:** ${benchmark_history.iloc[-1]:,.2f}")
                st.write("Tool Created by Alan ")
            except IndexError as e:
                st.error(f"An error occurred: {e}")

