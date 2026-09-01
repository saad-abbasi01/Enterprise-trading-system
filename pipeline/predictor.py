import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from pipeline.feature_engineer import TechnicalAnalysis
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score ,classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class MarketPredictor:
    def __init__(self):
        self.ta=TechnicalAnalysis()
        self.model=RandomForestClassifier(n_estimators=100,max_depth=10,random_state=42)
        self.feature_cols=[
            
            "SMA_20",
            "SMA_50",
            "RSI_14",
            "MACD",
            "MACD_Signal",
            "BB_Upper",
            "BB_Lower",
        ]
    def prepare_dataset(self,ticker:str)->pd.DataFrame:
        
        df=self.ta.compute_indicators(ticker)
        if df.empty:
            print(f"Data is not found in this dataframe of ticker:{ticker}")
            return pd.DataFrame()
        
        df["Target"]=(df["close_price"].shift(-1) > df["close_price"]).astype(int)
        cleaned_df=df.dropna().reset_index(drop=True)
        return cleaned_df
    def train_dataset(self,ticker:str):
        data=self.prepare_dataset(ticker)
        if data.empty:
            print("No dataset for training here.Dataset is compulsory")
            return 
        
        X=data[self.feature_cols]   
        Y=data["Target"]
        X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.30,shuffle=False)
        self.model.fit(X_train,Y_train)
        #now predict the trained model for checking
        prediction=self.model.predict(X_test)
        
        accuracy=accuracy_score(prediction,Y_test)
        print(f"Accuracy Score: {accuracy * 100:.2f}%\n")
        print("Classification Report:")
        print(classification_report(Y_test, prediction))

        return accuracy


if __name__ == "__main__":
    predictor = MarketPredictor()
    predictor.train_dataset("AAPL")
           