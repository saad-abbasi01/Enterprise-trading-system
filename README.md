# Enterprise Algorithmic Trading & Risk Management System

A modular, production-ready quantitative trading architecture built in Python. This system integrates MySQL relational storage, technical indicator feature engineering, Random Forest machine learning models, ATR-based risk management, and an interactive Streamlit executive dashboard.

---

## 🛠️ Architecture & Tech Stack

* **Language:** Python 3.10+
* **Database:** MySQL (XAMPP / MySQL Connector)
* **Data Processing & Analytics:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (RandomForestClassifier)
* **Visualization & UI:** Streamlit, Plotly
* **Version Control:** Git & GitHub

---

## 📁 Repository Structure

```text
Enterprise_trading_system/
│
├── config/
│   └── settings.py              # Environment and database config settings
│
├── database/
│   ├── db_connector.py          # MySQL connection pooling setup
│   └── models.py                # CRUD repository for fetching & seeding market data
│
├── pipeline/
│   ├── feature_engineer.py      # Computes SMA, RSI, MACD, and Bollinger Bands
│   └── predictor.py             # Random Forest classification pipeline (~69% accuracy)
│
├── services/
│   ├── risk_engine.py           # Calculates position sizing & ATR volatility exits
│   └── strategy_execution.py    # Core execution pipeline unifying ML signals and risk
│
├── app.py                       # Interactive Streamlit Web Terminal
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation