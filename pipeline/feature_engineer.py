import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from database.models import MarketDataRepository


class TechnicalAnalysis:

    def __init__(self):
        self.repo = MarketDataRepository()

    def compute_indicators(self, ticker: str) -> pd.DataFrame:
        """Fetches market data for a given ticker from MySQL and computes

        SMA, RSI, MACD, and Bollinger Bands.
        """
        df = self.repo.fetch_market_data(ticker)

        if df.empty:
            print(f"No market data found in the database for ticker: {ticker}")
            return pd.DataFrame()

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)

        # 1. Simple Moving Averages (SMA)
        df["SMA_20"] = df["close_price"].rolling(window=20).mean()
        df["SMA_50"] = df["close_price"].rolling(window=50).mean()

        # 2. Relative Strength Index (RSI - 14 Period)
        delta = df["close_price"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI_14"] = 100 - (100 / (1 + rs))

        # 3. Moving Average Convergence Divergence (MACD)
        ema_12 = df["close_price"].ewm(span=12, adjust=False).mean()
        ema_26 = df["close_price"].ewm(span=26, adjust=False).mean()
        df["MACD"] = ema_12 - ema_26
        df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
        df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]

        # 4. Bollinger Bands (20-day, 2 Std Dev)
        std_20 = df["close_price"].rolling(window=20).std()
        df["BB_Upper"] = df["SMA_20"] + (std_20 * 2)
        df["BB_Lower"] = df["SMA_20"] - (std_20 * 2)

        return df


if __name__ == "__main__":
    ta = TechnicalAnalysis()
    # Replace 'AAPL' with a ticker present in your MySQL database
    processed_df = ta.compute_indicators("AAPL")
    print(processed_df.tail())
        