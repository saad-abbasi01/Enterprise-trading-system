import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    
    
    
    #Db credentials
    DB_HOST:str=os.getenv("DB_HOST","127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER:str=os.getenv("DB_USER","root")
    DB_PASSWORD:str=os.getenv("DB_PASSWORD","")
    DB_NAME:str=os.getenv("DB_NAME","enterprise_trading_system")
    
    #Default system
    
    DEFAULT_TICKER:str=os.getenv("DEFAULT_TICKER","AAPL")
    DEFAULT_TIMEFRAME:str=os.getenv("DEFAULT_TIMEFRAME","1y")
    DEFAULT_MAX_DRAWDOWN:float=float(os.getenv("DEFAULT_MAX_DRAWDOWN",0.15))
    
settings=Settings()
print(f'Config Loaded: {settings.DB_NAME} on {settings.DB_HOST}')