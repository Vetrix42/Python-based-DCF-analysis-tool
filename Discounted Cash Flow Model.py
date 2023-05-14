import requests

# Function to fetch stock data using Alpha Vantage API
def fetch_stock_data(ticker):
    api_key = "3O6G6A69J6IK5AFT"  # Replace with your Alpha Vantage API key
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key,
    }

    # Send GET request to Alpha Vantage API to retrieve stock data
    response = requests.get(base_url, params=params)
    data = response.json()

    # Check if valid data is received
    if 'Monthly Adjusted Time Series' not in data:
        return None

    # Extract dividend data from the API response
    monthly_data = data['Monthly Adjusted Time Series']
    dividends = [float(monthly_data[date]['7. dividend amount']) for date in monthly_data]

    return dividends


def calculate_discounted_cash_flow(ticker, discount_rate, growth_rate, stock_compensation):
    # Fetch stock dividend data using the provided function
    dividends = fetch_stock_data(ticker)

    # Check if valid dividend data is received
    if dividends is None:
        return None

    free_cash_flows = []
    discounted_cash_flows = []
    terminal_value = 0

    # Calculate free cash flows and discounted cash flows for each dividend
    for i, div in enumerate(dividends):
        # Calculate cumulative free cash flow per share
        fcf_per_share = (sum(dividends[:i+1]) - stock_compensation) / (i + 1)
        free_cash_flows.append(fcf_per_share)

        # Calculate discounted cash flow per share based on the discount rate
        discounted_cash_flow = fcf_per_share / ((1 + discount_rate) ** i)
        discounted_cash_flows.append(discounted_cash_flow)

    # Calculate terminal value per share based on the last dividend
    last_dividend = dividends[-1]
    terminal_value_per_share = (last_dividend * (1 + growth_rate)) / (discount_rate - growth_rate)
    discounted_cash_flows.append(terminal_value_per_share / ((1 + discount_rate) ** len(dividends)))

    # Calculate the intrinsic value by summing discounted cash flows
    intrinsic_value = sum(discounted_cash_flows)

    return intrinsic_value, free_cash_flows, discounted_cash_flows


def calculate_200_day_moving_average(ticker):
    api_key = "3O6G6A69J6IK5AFT"  # Replace with your Alpha Vantage API key
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key,
    }

    # Send GET request to Alpha Vantage API to retrieve daily stock data
    response = requests.get(base_url, params=params)
    data = response.json()

    # Check if valid data is received
    if 'Time Series (Daily)' not in data:
        return None

    # Extract closing prices from the API response
    daily_data = data['Time Series (Daily)']
    closing_prices = [float(daily_data[date]['4. close']) for date in daily_data]

    # Calculate the 200-day moving average
    if len(closing_prices) >= 200:
        ma_200 = sum(closing_prices[-200:])

