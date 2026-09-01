import numpy as np

class RiskManager:
    
    def __init__(self,account_balance:float=100000.0,max_risk_per_trade:float=0.2):
        self.account_balance=account_balance
        self.max_risk_per_trade=max_risk_per_trade
        
    def calculate_position_size(self,entry_prize:float,sl_prize:float)->tuple[int,float]:
        
        risk_per_share=abs(float(entry_prize) - float(sl_prize))
        if risk_per_share <= 0:
            return 0,0.0
        max_allowed_risk=self.account_balance * self.max_risk_per_trade
        position_size=int(max_allowed_risk / risk_per_share)
        
        return position_size, round(position_size * risk_per_share, 2) 
    def calculate_exit_levels(self,entry_price:float,atr:float,multiplier:float=2.0):
        stop_loss=float(entry_price) - (float(atr) *float(multiplier))
        take_profit=float(entry_price) + (float(atr) *float(multiplier)*1.5)
        
        return round(stop_loss,2),round(take_profit,2)
if __name__ =="__main__":
    
    risk_agr=RiskManager(account_balance=100000.0)
    entry_price=250
    atr_val=2.5
    sl,tp=risk_agr.calculate_exit_levels(entry_price,atr_val)
    share, dollar_risk = risk_agr.calculate_position_size(entry_price,sl)
    
    print("Risk _manager_Evaluation")
    print(f"Entry_prize:{entry_price}")
    print(f"Stop_loss:{sl}")
    print(f"Recommended position_size is:{share} shares (risking ${dollar_risk})")