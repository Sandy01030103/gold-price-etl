import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime

# Add the project root directory to the Python path
# This allows the script to be run from anywhere, including from within the 'src' directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

DB_PATH = 'data/gold_prices.db' # 資料庫的位址
CHARTS_DIR = 'charts' # 畫出來的圖片要放到的位址

def generate_trend_chart():
    """
    Reads gold price data from the database and generates a trend chart.
    The chart is saved to the 'charts' directory with a timestamp.
    """
    os.makedirs(CHARTS_DIR, exist_ok=True)

    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at '{DB_PATH}'.")
        print("Please run the main ETL script (main.py) first to collect some data.")
        return

    try:
        # Connect to the database and read data into a pandas DataFrame
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT fetch_time, bank_selling_price FROM gold_prices WHERE status='OK' ORDER BY fetch_time DESC LIMIT 10", conn)
        conn.close()

        if df.empty:
            print("No data available in the database to generate a chart.")
            return

        # Convert fetch_time to datetime objects for plotting
        df['fetch_time'] = pd.to_datetime(df['fetch_time'])

        # Plotting
        plt.style.use('ggplot')
        plt.figure(figsize=(12, 6))
        plt.plot(df['fetch_time'], df['bank_selling_price'], marker='o', linestyle='-', color='gold')
        plt.title('Gold Price Trend (Bank Selling Price)', fontsize=16)
        plt.xlabel('Date and Time', fontsize=12)
        plt.ylabel('Bank Selling Price (TWD)', fontsize=12)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the chart with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_filename = os.path.join(CHARTS_DIR, f'trend_chart_{timestamp}.png')
        plt.savefig(chart_filename)
        print(f"Successfully generated and saved trend chart to '{chart_filename}'")

    except Exception as e:
        print(f"An error occurred while generating the chart: {e}")

if __name__ == "__main__":
    print(f"project root: {project_root}")
    generate_trend_chart()