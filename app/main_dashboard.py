import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go


#page_config of our dashboard
st.set_page_config(page_title="Enterprise Trading system & Risk management",page_icon="📊",layout="wide")

#Side bar  control
st.sidebar.title("Control Panel")
st.sidebar.markdown("-------")

#side bar input from user

ticker=st.sidebar.text_input("Assest ticker symbol",value="AAPL")
timeframe=st.sidebar.selectbox("Select TimeFrame:",["1 mon","3 mon","6 mon","1 yr","2 yr"])
risk_limit=st.sidebar.slider("Risk limit:",min_value=5,max_value=30,value=15)

st.sidebar.markdown("-----")
st.sidebar.info("**Enterprise Tip** This input will trigger automated risk check and signal accross all pipeline modules")

#Main dashboard system 
st.title("Enterprise Algorithm Trading & Risk Management System")
st.write(f"Live moniter for **{ticker.upper()}** | **{timeframe.upper()}** | **{risk_limit}**")
# Creating columns
col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric(label="Current_price",value="$185.50",delta="+2.35%")
with col2:
    st.metric(label="Predicted Trend",value="BULLISH",delta="82% Confidence")
with col3:
    st.metric(label="Value at Risk (VaR 95%)",value="$-4,250",delta="-2.1%",delta_color="inverse")
    
with col4:
    st.metric(label="Sharpe ratio",value="1.84",delta="Healthy")
    
st.markdown("----")

# table navgation
tab1,tab2,tab3=st.tabs(["Market Data & Indicators","ML Signal Predictor","Risk Engine"])

with tab1:
    st.subheader(f"Price Action & Moving average:**{ticker.upper()}**")
    
    #setting...
    dates=pd.date_range(end=pd.Timestamp.today(), periods=100)
    prices=np.cumsum(np.random.randn((100))+ 100)
    df_sim=pd.DataFrame({"Date":dates,"Close":prices})
    
    #preview chart layout
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df_sim['Date'],y=df_sim['Close'],mode="lines",name="Close price",line=dict(color="#00FFAA")))
    fig.update_layout(template= "plotly_dark",height=400,margin=dict(l=20,r=20,t=3000,b=20))
    
    st.plotly_chart(fig,use_container_width=True)
    
    #Table 2
    with tab2:
        st.title("Machine Learning Direction Forcast")
        col_left,col_right=st.columns(2)
        with col_left:
            st.write("**Model Features Evaluated:**")
        st.write("• Relative Strength Index (RSI)")
        st.write("• Moving Average Convergence Divergence (MACD)")
        st.write("• 20-Day Volatility Standard Deviation")
        if st.button("Run ML Model Inference"):
            st.success("Signal Generated: **BUY / LONG**")
            
    with col_right:
        st.info("The prediction module uses a Random Forest Classifier trained on technical indicators to estimate probability of a positive return over the next 5 trading days.")
    #Third model
    with tab3:
        st.subheader("Enterprise Risk Management Controls")
        st.warning(f"Configured Drawdown Limit:**{risk_limit}%**")
        st.write("The Risk Engine continously calculates Values_at_Risk(VaR) and maximum drawdown to automatically halt trading if capital threshold limit breached")