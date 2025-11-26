import sqlite3
import os
from datetime import datetime

class DBManager:
    """Manages all database operations for the gold price data."""

    def __init__(self, db_path: str):
        """
        Initializes the DBManager.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def _get_connection(self):
        """Establishes and returns a database connection."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Creates the gold_prices table if it doesn't already exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gold_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fetch_time DATETIME NOT NULL,
                    bank_selling_price REAL NOT NULL,
                    bank_buying_price REAL NOT NULL,
                    status TEXT NOT NULL
                )
            """)
            conn.commit()

    def insert_price(self, fetch_time: datetime, bank_selling_price: float, bank_buying_price: float, status: str):
        """
        Inserts a new price record into the database.

        Args:
            fetch_time (datetime): The timestamp of when the data was fetched.
            bank_selling_price (float): The cleaned bank selling price.
            bank_buying_price (float): The cleaned bank buying price.
            status (str): The status of the data ('OK').
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gold_prices (fetch_time, bank_selling_price, bank_buying_price, status) VALUES (?, ?, ?, ?)",
                (fetch_time, bank_selling_price, bank_buying_price, status)
            )
            conn.commit()