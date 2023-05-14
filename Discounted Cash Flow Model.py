import requests

def fetch_stock_data(ticker):
    api_key = "3O6G6A69J6IK5AFT"  # Replace with your Alpha Vantage API key
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'Monthly Adjusted Time Series' not in data:
        return None

    monthly_data = data['Monthly Adjusted Time Series']
    dividends = [float(monthly_data[date]['7. dividend amount']) for date in monthly_data]

    return dividends

def calculate_discounted_cash_flow(ticker, discount_rate, growth_rate):
    dividends = fetch_stock_data(ticker)

    if dividends is None:
        return None

    free_cash_flows = []
    discounted_cash_flows = []
    terminal_value = 0

    for i, div in enumerate(dividends):
        free_cash_flow = sum(dividends[:i+1])
        free_cash_flows.append(free_cash_flow)

        discounted_cash_flow = div / ((1 + discount_rate) ** i)
        discounted_cash_flows.append(discounted_cash_flow)

    last_dividend = dividends[-1]
    terminal_value = (last_dividend * (1 + growth_rate)) / (discount_rate - growth_rate)
    discounted_cash_flows.append(terminal_value / ((1 + discount_rate) ** len(dividends)))

    intrinsic_value = sum(discounted_cash_flows)

    return intrinsic_value, free_cash_flows, discounted_cash_flows

# Example usage
ticker = "AAPL"  # Replace with the desired stock ticker
discount_rate = 0.1  # Replace with your desired discount rate
growth_rate = 0.05  # Replace with your desired growth rate

intrinsic_value, free_cash_flows, discounted_cash_flows = calculate_discounted_cash_flow(ticker, discount_rate, growth_rate)

# Print the results
print("Intrinsic Value:", intrinsic_value)
print("\nFree Cash Flows:")
print(free_cash_flows)
print("\nDiscounted Cash Flows:")
print(discounted_cash_flows)