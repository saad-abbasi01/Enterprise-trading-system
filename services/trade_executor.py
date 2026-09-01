import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from pipeline.feature_engineer import TechnicalAnalysis
from pipeline.predictor import MarketPredictor
from services.risk_engine import RiskManager

class StrategyExecutionEngine:
    
    def __init__(self,account_balance : float=10000.0):
        self.ta=TechnicalAnalysis()
        self.predictor=MarketPredictor()
        self.risk_mgr=RiskManager()
        
    def execute_trade_signal(self,ticker:str):
        
        print(f"\n==========================================")
        print(f" Executing Strategy Pipeline for: {ticker}")
        print(f"==========================================")
        
        df=self.ta.compute_indicators(ticker)
        #if no data return nothing
        if df.empty:
            print(f"Aborting program!! no data in the dataframe for {ticker}")
            return
        latest_row=df.iloc[[-1]]
        current_price=float(latest_row['close_price'])
        self.predictor.train_dataset(ticker)
        X_latest=df[self.predictor.feature_cols].iloc[[-1]]
        signal=self.predictor.model.predict(X_latest)[0]
        
        signal_str="Buy" if signal==1 else "Sell"
        print(f" [ML Predictor] Current price:{current_price:.2f}")
        print(f"[ML Predictor] Signal Output:{signal_str}")
        atr_estimate=float(df["close_price"].rolling(14).std().iloc[-1])
        if round(atr_estimate,2) == 0:
            atr_estimate=2.5
        stop_loss,Take_profit=self.risk_mgr.calculate_exit_levels(current_price,atr_estimate)
        
        #calculate risk per share
        
        risk_per_share,shares=self.risk_mgr.calculate_position_size(current_price,stop_loss)
        
        print("\n---------------- ORDER SHEET ----------------")
        print(f"Ticker Symbol   : {ticker}")
        print(f"Action Signal   : {signal_str}")
        print(f"Entry Price     : ${current_price:.2f}")
        print(f"Stop Loss       : ${stop_loss:.2f}")
        print(f"Take Profit     : ${Take_profit:.2f}")
        print(f"Risk Per Share  : ${risk_per_share:.2f}")
        print(f"Order Volume    : {shares} shares")
        print("---------------------------------------------\n")


if __name__ == "__main__":
    engine = StrategyExecutionEngine(account_balance=100000.0)
    engine.execute_trade_signal("AAPL")
            