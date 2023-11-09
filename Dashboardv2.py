from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.palettes import Spectral11
import requests
import time

# Function to fetch and update data
def update_data():
    while True:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()

                # Sort and trim data to ensure a consistent length of 10 items
                top_gainers = sorted(data, key=lambda x: float(x['priceChangePercent']), reverse=True)[:10]
                top_losers = sorted (data, key=lambda x: float(x['priceChangePercent']))[:10]
                top_volume = sorted(data, key=lambda x: float(x['quoteVolume']), reverse=True)[:10]

                # Extract data for visualization
                trading_pairs_gainers = [pair['symbol'] for pair in top_gainers]
                price_changes_gainers = [float(pair['priceChangePercent']) for pair in top_gainers]
                trading_pairs_losers = [pair['symbol'] for pair in top_losers]
                price_changes_losers = [float(pair['priceChangePercent']) for pair in top_losers]
                trading_pairs_volume = [pair['symbol'] for pair in top_volume]
                volume = [float(pair['quoteVolume']) for pair in top_volume]

                # Ensure all lists have the same length (in this case, 10)
                min_length = 10
                trading_pairs_gainers = trading_pairs_gainers[:min_length]
                price_changes_gainers = price_changes_gainers[:min_length]
                trading_pairs_losers = trading_pairs_losers[:min_length]
                price_changes_losers = price_changes_losers[:min_length]
                trading_pairs_volume = trading_pairs_volume[:min_length]
                volume = volume[:min_length]

                # Sleep for 5 minutes before the next update
                time.sleep(300)  # 300 seconds (5 minutes)
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Binance Futures API URL for 24-hour price statistics
api_url = 'https://fapi.binance.com/fapi/v1/ticker/24hr'

# Initialize data sources
source_gainers = ColumnDataSource(data=dict(trading_pairs=[], price_changes=[], color=[]))
source_losers = ColumnDataSource(data=dict(trading_pairs=[], price_changes=[], color=[]))
source_volume = ColumnDataSource(data=dict(trading_pairs=[], volume=[], color=[]))

# Create bar charts for gainers, losers, and volume
p_gainers = figure(x_range=[], height=350, title="Top Gainers - Binance Perpetual Futures")
p_gainers.vbar(x='trading_pairs', top='price_changes', width=0.6, source=source_gainers, line_color="white", fill_color='color', legend_label="Gainers")

p_losers = figure(x_range=[], height=350, title="Top Losers - Binance Perpetual Futures")
p_losers.vbar(x='trading_pairs', top='price_changes', width=0.6, source=source_losers, line_color="white", fill_color='color', legend_label="Losers")

p_volume = figure(x_range=[], height=350, title="Top Volume - Binance Perpetual Futures")
p_volume.vbar(x='trading_pairs', top='volume', width=0.6, source=source_volume, line_color="white", fill_color='color', legend_label="Volume")

# Create the layout
layout = column(
    row(p_gainers, p_losers, p_volume),
)

curdoc().add_root(layout)

# Start updating data
update_data()
