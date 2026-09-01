import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import yfinance as yf
from database.models import MarketDataRepository

class DataFetcher:
    
    def __init__(self):
        self.repo=MarketDataRepository()
        
    def fetch_and_store_ticker(self,ticker:str,period:str="1mo",interval:str="1d") ->pd.DataFrame:
        print(f"fetch data for {ticker} and {period}")
        
        stock=yf.Ticker(ticker)
        df=stock.history(period=period,interval=interval)
        if df.empty:
            print(f"No data for Ticker{ticker}")
            return pd.DataFrame()
        
        df=df.reset_index()
        df['ticker']=ticker.upper()
        
        date_col="Date" if "Date" in df.columns else "Datetime"
        df["timestamp"]=pd.to_datetime(df[date_col]).dt.strftime("%Y/%m/%d %H:%M:%S")
        
        df=df.rename(
            
            columns={
                "Open": "open_price",
                "High":"high_price",
                "Low":"low_price",
                "Close":"close_price",
                "Volume":"volume",
    
            }
        )
        required_cols=["ticker","timestamp","open_price","high_price","low_price","close_price","volume"]
        
        clean_df=df[required_cols]
        
        success=self.repo.insert_market_data(clean_df)
        
        if success:
            print(f"Real time pipeline execution completed for {ticker}")
            return clean_df
        else:
            print(f"Failed to persist data for {ticker}")
            return pd.DataFrame()
        
if __name__ == "__main__":
    fetcher=DataFetcher()
    data = fetcher.fetch_and_store_ticker(ticker="AAPL", period="1mo", interval="1d")

    if not data.empty:
        print("\n📊 First 5 rows of fetched live data:")
        print(data.head())