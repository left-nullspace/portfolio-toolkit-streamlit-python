
#storing all the big bodies of text here for the optimization tool
class OptContent:

    @staticmethod
    def howToUse():
        return """
        ### Step-by-Step Instructions for Using the Portfolio Optimizer:

        **1. Set Start and End Date:**
        - Go to the sidebar and set the start and end dates for the period over which you want to analyze and optimize your portfolio. These dates define the historical data range that will be used for calculations.

        **2. Set Initial Portfolio Value:**
        - Specify how much money you're starting with in your portfolio. This is your initial investment amount. Enter this value in the sidebar.

        **3. Set Benchmark:**
        - Choose a benchmark ETF from the sidebar dropdown. This ETF is what we'll compare our portfolio's performance against. It helps to see if our optimized portfolio is performing better or worse than a common market index or a standard investment choice.

        **4. Enter Stock Tickers:**
        - Input the symbols of the stocks or assets you want to include in your portfolio in a comma-separated list. For example, you might enter: `SPY, TLT, GLD, AAPL, TSLA, QQQ, BTC-USD`. These tickers represent the assets you're considering for investment, and you can find valid ticker symbols on financial websites like [Yahoo Finance](https://finance.yahoo.com/).

        **5. Select 'Optimize Portfolio' and Analyze the Results:**
        - After entering your data, click the 'Optimize Portfolio' button. This will calculate and display the optimal allocations for two types of portfolios:
            - **Maximum Sharpe Ratio Portfolio:** Best Return/Risk ratio — think of it as a choice for the more adventurous investor.
            - **Minimum Volatility Portfolio:** Lowest possible risk for the expected return. It's great for more conservative investors who prefer stability, like someone who prioritizes preservation of capital over high returns.
        """

    @staticmethod
    def importantDefinitions():
        return """
        ### Portfolio Insights:

        **Understanding the Process:**
        - We calculate returns and risks for various asset weightings, plotting them on a scatter plot. Through **optimization**, we identify the 'Efficient Frontier' — the best return for a given risk level. From this, we derive the **Maximum Sharpe Ratio** portfolio, which offers the highest return per unit of risk. Learn more about the Efficient Frontier [here](https://www.investopedia.com/terms/e/efficientfrontier.asp).
        - The library used for the optimization is [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/en/latest/)
        
        **📈 Maximum Sharpe Ratio Portfolio:**
        - This portfolio provides the best risk-adjusted return. For instance, a Sharpe ratio of 1.5 means 1.5 units of gain for each unit of risk. It's ideal for those seeking maximum growth with controlled risk.

        **🛡️ Minimum Volatility Portfolio:**
        - Designed to minimize risk for a given return level, this portfolio is suited for risk-averse investors seeking stability.

        **📊 Analyze Performances:**
        - View the historically backtested performance of these portfolios over your selected period to see potential long-term growth.
        """


    @staticmethod  
    def exampleWalkthrough():
        return """
        ### Example Walkthrough: Optimizing a Diverse Portfolio

        #### Process:
        1. **Stock Tickers Entered:** `SPY, TLT, GLD, BTC-USD, TSLA, QQQ`
           - These represent a mix of asset classes including large-cap stocks (SPY, QQQ), government bonds (TLT), gold (GLD), cryptocurrency (BTC-USD), and high-tech stocks (TSLA).

        2. **Select Date Range:**
           - Choose a historical period over which you want to analyze and optimize the portfolio. The start date will automatically adjust to the earliest date for which all selected assets have available data. This ensures that the analysis is based on a complete dataset for all included assets.

        3. **Enter Initial Portfolio Value:**
           - Set an amount you are planning to invest. This could be any starting value that fits your investment plan.

        4. **Optimize Portfolio:**
           - Click on the 'Optimize Portfolio' button to generate the optimal asset allocations based on historical data.

        #### Analyzing Results:
        - The tool uses the data from the specified period to calculate two main types of portfolios: Maximum Sharpe Ratio and Minimum Volatility. Lets go through an example output:

        **📈 Maximum Sharpe Ratio Portfolio:**
        - This portfolio configuration is designed to offer the highest return for the risk taken.
        - **Weights:**
          - `QQQ`: 43% (Tech-heavy stocks indicating a preference for growth)
          - `GLD`: 32% (Gold, typically a safe haven during market turbulence)
          - `BTC-USD`: 21% (High-risk, high-reward asset)
          - `TSLA`: 4% (High growth potential but volatile)
          - `TLT`: 0% (No allocation to bonds, indicating a more aggressive strategy)
          - `SPY`: 0% (No allocation to broad market index, focusing on more specific sectors)
        - The absence of traditional bonds and broad market indices like SPY in this portfolio highlights a strategic focus on higher growth and technology-oriented assets.

        **🛡️ Minimum Volatility Portfolio:**
        - This portfolio aims to minimize risk while providing reasonable returns.
        - **Weights:**
          - `TLT`: 37% (Heavy allocation towards bonds, emphasizing safety)
          - `SPY`: 34% (Stable, broad market exposure)
          - `GLD`: 29% (Continued preference for the stability of gold)
          - `BTC-USD`: 0% (Avoids the volatility of cryptocurrencies)
          - `QQQ`: 0% (No exposure to tech-heavy stocks, reducing risk)
          - `TSLA`: 0% (Avoids the high volatility associated with Tesla)
        - The focus on bonds and gold, with no allocation towards high-volatility assets like tech stocks or cryptocurrencies, suggests a conservative approach, aiming to preserve capital with minimal fluctuations.

        **Blended Strategy:**
        - While each portfolio targets specific risk preferences, a blended approach may appeal to investors looking for a balance between growth and safety. 
        By combining elements of both the Maximum Sharpe Ratio and Minimum Volatility portfolios, investors can tailor their exposure to match their individual risk tolerance and investment goals.
        """