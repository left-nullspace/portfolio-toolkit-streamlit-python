class SimContent:
    @staticmethod
    def howToUse():
        return """
        ### Step-by-Step Instructions for Using the Portfolio Simulator:

        **1. Set Start and End Date:**
        - Specify the period over which you want to analyze your portfolio's performance. Adjust the start and end dates in the sidebar to set the range of historical data that will be used.

        **2. Enter Initial Portfolio Value:**
        - Set the initial amount of money you are investing in the sidebar. This figure represents your starting capital.

        **3. Select Benchmark:**
        - Choose a benchmark ETF from the sidebar dropdown to compare your portfolio’s performance against. This helps evaluate whether your strategy outperforms common market indices.

        **4. Enter Stock Tickers:**
        - Input the symbols of the stocks or assets you want to simulate in your portfolio. Enter them in a comma-separated list in the sidebar. For example: `SPY, TLT, GLD, BTC-USD, TSLA, QQQ`.

        **5. Enter Initial Weights:**
        - Define how much of your total investment should be allocated to each asset, ensuring that the percentages add up to 100%. For example: `30%, 20%, 10%, 20%, 10%, 10%`.

        **6. Select Rebalance Period:**
        - Choose how often you want to adjust your portfolio back to these initial weights. Options include annually, semi-annually, quarterly, monthly, or not at all, allowing you to simulate the effect of different rebalancing strategies on your investment's performance.
        """

    @staticmethod
    def insights():
        return """
        ### Portfolio Insights:

        **📈 Performance Metrics:**
        - Simulate and analyze various performance metrics such as expected annual return, annual volatility, and the Sharpe Ratio, giving you insights into the risk-adjusted returns of your strategy.

        **📊 Portfolio Balance Over Time:**
        - Observe how your portfolio's balance evolves over time with or without regular rebalancing. Graphical representations will highlight the portfolio's response to market changes, and red vertical lines will mark rebalancing events.

        **🛡️ Risk Management:**
        - Learn how strategic rebalancing can help manage risk and align your portfolio with your financial goals, maintaining desired asset proportions and adjusting to market shifts.
        """

    @staticmethod
    def exampleWalkthrough1():
        return """
        ### Example Walkthrough 1: 60/40 Stock-Bond Split with Annual Rebalancing

        **Overview:**
        - The [60/40 portfolio](https://www.experian.com/blogs/ask-experian/what-is-60-40-portfolio/) is a classic investment strategy where 60% of your money is in stocks (for growth) and 40% is in bonds (for stability). This mix aims to offer a balance between earning potential and risk reduction.

        **Setting Up Your Portfolio:**
        - **Tickers and Weights:** Enter `SPY` (60%), `TLT` (40%) in the tool.
        - **How to Enter Data:** Type the tickers as `SPY, TLT` and weights as `0.60, 0.40` in the input fields.
        - **Rebalancing Frequency:** Once a year (Annually).
        - **Investment Period:** From January 1, 2010, to December 31, 2020.

        **Rebalancing Explanation:**
        - Imagine starting with 10000: investing 6000 in SPY and 4000 in TLT.
        - **End of Year 1:** Let’s say SPY grows to 6600 and TLT to 4200, making your portfolio total 10800.
        - **Rebalancing Goal:** To maintain your 60/40 split, you need to adjust the amounts to keep the same ratio.
        - **Action:** Move 120 from SPY (which has grown more) to TLT (to restore the 60/40 balance).

        **Simulate Portfolio:**
        - After setting up your portfolio and understanding the rebalancing process, click the "Simulate Portfolio" button to see how your investments perform over the specified period.
        """

    @staticmethod
    def exampleWalkthrough2():
        return """
        ### Example Walkthrough 2: Ray Dalio's All Weather Portfolio

        **Overview:**
        - Ray Dalio's [All Weather Portfolio](https://www.robomarkets.com/blog/investing/strategies/understanding-ray-dalios-all-weather-portfolio-a-diversified-investment-approach/) is designed to perform steadily in different economic conditions by diversifying across various asset classes.

        **Setting Up Your Portfolio:**
        - **Tickers and Weights:** Enter `SPY` (30%), `GLD` (15%), `TLT` (40%), `TIP` (7.5%), `DBC` (7.5%).
        - **How to Enter Data:** Type the tickers as `SPY, GLD, TLT, TIP, DBC` and weights as `0.30, 0.15, 0.40, 0.075, 0.075`.
        - **Rebalancing Frequency:** Once a year (Annually).
        - **Investment Period:** From January 1, 2010, to December 31, 2020.

        **Rebalancing Explanation:**
        - Refer to example 1, in short we readjust to the initial weights (`0.30, 0.15, 0.40, 0.075, 0.075`) once a year

        **Simulate Portfolio:**
        - After setting up your portfolio and understanding the rebalancing process, click the "Simulate Portfolio" button to see how the All Weather Portfolio performed over the specified period.

        """