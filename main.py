import os
import sys
import logging
from datetime import datetime

# Add the project root directory to the Python path to resolve module imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.scraper import fetch_gold_price
from src.cleaner import clean_and_validate_price
from src.db_manager import DBManager

# --- Configuration ---
LOGS_DIR = 'logs'
DB_PATH = 'data/gold_prices.db'

# --- Setup Logging ---
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, 'etl_monitor.log')),
        logging.StreamHandler()
    ]
)

def main():
    """
    Main ETL process to fetch, clean, and store gold price data.
    """
    logging.info("Starting ETL process...")
    db_manager = DBManager(DB_PATH)
    db_manager.init_db()

    try:
        # 1. Extract
        raw_price = fetch_gold_price()
        logging.info(f"Successfully fetched raw data: '{raw_price}'")

        # 2. Transform
        cleaned_price, status = clean_and_validate_price(raw_price)
        logging.info(f"Data validation result: Price={cleaned_price}, Status={status}")

        # 3. Load
        if status == 'OK':
            fetch_time = datetime.now()
            db_manager.insert_price(fetch_time, cleaned_price, status)
            logging.info("Successfully inserted data into the database.")
        else:
            logging.warning("Data validation failed. Skipping database insertion.")

    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {e}", exc_info=True)

if __name__ == "__main__":
    main()