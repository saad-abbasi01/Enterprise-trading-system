
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import mysql.connector 
from mysql.connector import Error, pooling
from config.settings import settings


#creating class:

class Database_Connector:
    
    def __init__(self):
        try:
            self.pool=mysql.connector.pooling.MySQLConnectionPool(
                pool_name="trading_pool",
                pool_size=5,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME
            )
            print(f"Mysql connection is created successfully of: {settings.DB_NAME}")
        except Error  as e:
            print(f" Error initializing MYSQL connection  pool :{e}")
            
            self.pool=None
            
    def get_connection(self):
        #Simple condition for retrieve data
        if self.pool:
            return self.pool.get_connection()
        else:
            print("Nothing to return")
            
    def Create_tables(self):
        create_market_data_table="""
        CREATE TABLE IF NOT EXISTS market_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ticker VARCHAR(20) NOT NULL,
            timestamp DATETIME NOT NULL,
            open_price DECIMAL(12, 4),
            high_price DECIMAL(12, 4),
            low_price DECIMAL(12, 4),
            close_price DECIMAL(12, 4),
            volume BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_bar (ticker, timestamp)
        );
        """
        
        cursor=None
        conn=None
        try:
            conn=self.get_connection()
            cursor=conn.cursor()
            
            cursor.execute(create_market_data_table)
            conn.commit()
            print("Database table 'market_data' checked/created successfully")
        except Error as e:
            print(f"Error creating database table:{e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
db=Database_Connector()
if __name__=="__main__":
    db.Create_tables()
        