import os
import sys
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

# Add the project root directory to the Python path to resolve module imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.scraper import get_bot_gold_price
from src.cleaner import clean_and_validate_prices
from src.db_manager import DBManager

# --- Configuration ---
# 大寫表示不會改變值的變數
LOGS_DIR = 'logs' # DIR = directory資料夾
DB_PATH = 'data/gold_prices.db'
URL = "https://rate.bot.com.tw/gold/"

# --- Setup Logging ---
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO, # log的等級: debug, info, error
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
        raw_prices = get_bot_gold_price(URL) # 導到scraper.py
        logging.info(f"Successfully fetched raw data: {raw_prices}")

        # 2. Transform
        cleaned_prices, status = clean_and_validate_prices(raw_prices) # cleaned_prices, 'OK'
        logging.info(f"Data validation result: Prices={cleaned_prices}, Status={status}")

        # 3. Load
        if status == 'OK':
            fetch_time = datetime.now(ZoneInfo("Asia/Taipei")) # 現在的時間
            db_manager.insert_price(
                fetch_time,
                cleaned_prices["bank_selling_price"], # 清理好的賣出價格
                cleaned_prices["bank_buying_price"],  # 清理好買進價格
                status
            )
            logging.info("Successfully inserted data into the database.")
        else:
            logging.warning("Data validation failed. Skipping database insertion.")

    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {e}", exc_info=True)

if __name__ == "__main__":
    main()