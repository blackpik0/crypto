import requests
import time

# Binance Futures API URL for 24-hour price statistics
api_url = 'https://fapi.binance.com/fapi/v1/ticker/24hr'

while True:
    # Fetch 24-hour price statistics for all perpetual futures pairs
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

    # Sort by percentage price change, trading volume
    top_gainers = sorted(data, key=lambda x: float(x['priceChangePercent']), reverse=True)[:10]
    top_losers = sorted(data, key=lambda x: float(x['priceChangePercent']))[:10]
    top_volume = sorted(data, key=lambda x: float(x['volume']), reverse=True)[:10]

    print("Top Gainers:")
    for pair in top_gainers:
        print(f"{pair['symbol']} - Change: {float(pair['priceChangePercent']):.2f}%")

    print("\nTop Losers:")
    for pair in top_losers:
        print(f"{pair['symbol']} - Change: {float(pair['priceChangePercent']):.2f}%")

    print("\nTop Volume Trading Pairs:")
    for pair in top_volume:
        print(f"{pair['symbol']} - Volume: {float(pair['volume']):.2f}")

    time.sleep(60)  # Wait for 1 minute

else:
    print(f"Error: {response.status_code}")

    
