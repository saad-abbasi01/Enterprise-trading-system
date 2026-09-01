import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from database.db_connector import Database_Connector
from mysql.connector import Error


class MarketDataRepository:

    def __init__(self):
        self.db = Database_Connector()

    def insert_market_data(self, df: pd.DataFrame) -> bool:
        query = """
        INSERT INTO market_data 
        (ticker, timestamp, open_price, high_price, low_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            open_price = VALUES(open_price),
            high_price = VALUES(high_price),
            low_price = VALUES(low_price),
            close_price = VALUES(close_price),
            volume = VALUES(volume);
        """
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            data_tables = [
                (
                    row["ticker"],
                    row["timestamp"],
                    float(row["open_price"]),
                    float(row["high_price"]),
                    float(row["low_price"]),
                    float(row["close_price"]),
                    int(row["volume"]),
                )
                for _, row in df.iterrows()
            ]

            cursor.executemany(query, data_tables)
            conn.commit()
            print(
                f"✅ Successfully inserted/updated {cursor.rowcount} records in MySQL."
            )
            return True
        except Error as e:
            print(f"❌ Error inserting market data: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def fetch_market_data(self, ticker: str) -> pd.DataFrame:
        query = """
        SELECT timestamp, open_price, high_price, low_price, close_price, volume 
        FROM market_data 
        WHERE ticker = %s
        ORDER BY timestamp ASC;
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (ticker,))
            rows = cursor.fetchall()

            if not rows:
                return pd.DataFrame()

            return pd.DataFrame(rows)

        except Error as e:
            print(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()

        finally:
            if conn and conn.is_connected():
                conn.close()


if __name__ == "__main__":
    # Generated 100 periods so SMA_50 can compute without dropping all rows
    dates = pd.date_range(
        end=pd.Timestamp.now(), periods=100, freq="D"
    ).strftime("%Y-%m-%d %H:%M:%S")

    sample_df = pd.DataFrame(
        {
            "ticker": "AAPL",
            "timestamp": dates,
            "open_price": 150.0 + np.random.randn(100),
            "high_price": 155.0 + np.random.randn(100),
            "low_price": 148.0 + np.random.randn(100),
            "close_price": 152.0 + np.random.randn(100),
            "volume": np.random.randint(100000, 500000, size=100),
        }
    )

    repo = MarketDataRepository()
    repo.insert_market_data(sample_df)

    fetch_df = repo.fetch_market_data("AAPL")
    print("\nFetched market data from MySQL:")
    print(fetch_df.head())