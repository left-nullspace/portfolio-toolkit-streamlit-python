import pandas as pd
import numpy as np
import yfinance as yf

def load_and_prepare_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def rebalance_portfolio(file_paths, 
                        benchmark_file_path,
                        initial_balance, 
                        asset_weights, 
                        rebalance_period,
                        start_date=None,
                        end_date=None):
    datasets = [load_and_prepare_data(file_path, start_date, end_date) for file_path in file_paths]
    benchmark_data = load_and_prepare_data(benchmark_file_path, start_date, end_date)
    period_length = {
        'annually': 12,
        'semi-annually': 6,
        'quarterly': 3,
        'monthly': 1,
        'none': np.inf
    }[rebalance_period]

    portfolio_balance = initial_balance
    benchmark_balance = initial_balance
    asset_balances = [weight * initial_balance for weight in asset_weights]

    common_dates = sorted(set.intersection(*(set(df['Date']) for df in datasets), set(benchmark_data['Date'])))
    common_dates = [date for date in common_dates if (start_date is None or date >= pd.to_datetime(start_date)) and (end_date is None or date <= pd.to_datetime(end_date))]

    start_date = common_dates[0]
    last_rebalance_date = start_date

    portfolio_history = []
    benchmark_history = []
    rebalance_dates = []

    for date in common_dates:
        if date <= start_date:
            continue

        for i, df in enumerate(datasets):
            previous_price = df.loc[df['Date'] < date, 'Adj Close'].iloc[-1]
            current_price = df.loc[df['Date'] == date, 'Adj Close'].iloc[0]
            asset_balances[i] *= current_price / previous_price

        previous_price = benchmark_data.loc[benchmark_data['Date'] < date, 'Adj Close'].iloc[-1]
        current_price = benchmark_data.loc[benchmark_data['Date'] == date, 'Adj Close'].iloc[0]
        benchmark_balance *= current_price / previous_price

        portfolio_balance = sum(asset_balances)

        portfolio_history.append({'Date': date, 'Balance': portfolio_balance})
        benchmark_history.append({'Date': date, 'Balance': benchmark_balance})

        months_since_last_rebalance = (date.year - last_rebalance_date.year) * 12 + (date.month - last_rebalance_date.month)
        if months_since_last_rebalance >= period_length:
            desired_balances = [weight * portfolio_balance for weight in asset_weights]
            asset_balances = desired_balances
            last_rebalance_date = date
            rebalance_dates.append(date)

    portfolio_history = pd.DataFrame(portfolio_history).set_index('Date')['Balance']
    benchmark_history = pd.DataFrame(benchmark_history).set_index('Date')['Balance']

    return portfolio_history, benchmark_history, rebalance_dates

def calculate_cumulative_returns(data, weights, initial_value):
            returns = data.pct_change().dropna()
            portfolio_returns = returns.dot(weights)
            cumulative_returns = (1 + portfolio_returns).cumprod() * initial_value
            return cumulative_returns

def calculate_metrics(history):
                    returns = history.pct_change().dropna()
                    mean_return = returns.mean() * 252
                    std_dev = returns.std() * np.sqrt(252)
                    sharpe_ratio = mean_return / std_dev
                    return mean_return, std_dev, sharpe_ratio