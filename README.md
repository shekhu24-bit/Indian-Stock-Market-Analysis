# 📈 Indian Stock Market Analysis Dashboard

A Business Analytics project that combines **Python**, **Data Analysis**, and **Power BI** to evaluate leading Indian companies using historical stock prices, company fundamentals, and news sentiment indicators.

---

## 🎯 Project Objective

The objective of this project is to analyze the performance of major Indian stocks and provide data-driven investment insights through an interactive Power BI dashboard.

The project evaluates companies based on:

- Historical Stock Performance
- Market Capitalization
- PE Ratio Analysis
- Dividend Yield Comparison
- Daily Volatility (Risk Measurement)
- News Sentiment Analysis
- Sector-wise Comparison
- Investment Ranking Framework

---

## 🏢 Companies Analyzed

- Reliance Industries
- TCS
- Infosys
- HDFC Bank
- ICICI Bank
- SBI
- ITC
- Bharti Airtel
- Larsen & Toubro
- Hindustan Unilever

---

## 🛠 Technologies Used

**Data Generation & Analysis**
- Python 3
- Pandas
- NumPy
- Matplotlib

**Business Intelligence**
- Microsoft Power BI

**Data Storage**
- CSV Files

---

## 📂 Project Structure

```text
Indian_Stock_Market_Analysis/
│
├── dashboard.pbix
│
├── stock_prices.csv
├── company_fundamentals.csv
├── news_sentiment.csv
│
├── charts/
│   ├── investment_score.png
│   ├── sentiment_score.png
│   └── pe_vs_dividend.png
│
├── generate_dataset.py
├── analysis.py
├── charts.py
│
├── requirements.txt
└── README.md
```

---

## 📊 Dashboard Pages

**1️⃣ Executive Summary**

Provides a high-level overview of:

- Average Closing Price
- Total Market Capitalization
- Average PE Ratio
- Overall Sentiment Score
- Stock Price Trend Analysis

---

**2️⃣ Fundamental Analysis**

Evaluates companies based on:

- PE Ratio Comparison
- Dividend Yield Analysis
- Market Capitalization Distribution
- Sector-wise Comparison

---

**3️⃣ Sentiment Analysis**

Analyzes market perception using:

- Average News Sentiment Score
- Positive vs Negative News Distribution

---

**4️⃣ Investment Recommendation**

Investment Score is calculated using:

```text
Investment Score =
(Sentiment Score x 40)
+ (100 - PE Ratio)
+ (Dividend Yield x 5)
```

Companies are ranked according to:

- Market Sentiment
- Valuation Metrics
- Dividend Performance

---

## 📈 Dataset Information

**Stock Price Dataset**

- Date, Company, Open, High, Low, Close, Volume
- 3650+ Records

**Company Fundamentals Dataset**

- Company, Sector, Market Cap, PE Ratio, Dividend Yield
- 10 Companies

**News Sentiment Dataset**

- Date, Company, Headline, Sentiment Score, Sentiment
- 500+ Records

---

## 🚀 How To Run

**Step 1 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 2 — Generate datasets**

```bash
python generate_dataset.py
```

**Step 3 — Run analytical report**

```bash
python analysis.py
```

**Step 4 — Generate charts**

```bash
python charts.py
```

**Step 5 — Open Power BI**

Open `dashboard.pbix` in Power BI Desktop and click **Home → Refresh**.

---

## 🔍 Key Insights

- HDFC Bank ranked #1 with the highest Investment Score.
- Bharti Airtel has the most positive news sentiment.
- Reliance Industries offers the best valuation with lowest PE Ratio.
- Banking sector shows the most balanced PE and Dividend metrics.
- Overall 61.8% of news coverage was positive across all companies.

---

## 💼 Business Applications

- Investment Research
- Portfolio Evaluation
- Financial Analytics
- Business Intelligence Reporting
- MBA Business Analytics Projects

---

## 📚 Learning Outcomes

- Data Cleaning and Processing
- Financial Data Analysis
- Volatility and Risk Measurement
- Sentiment Analysis
- Matplotlib Chart Generation
- Power BI Dashboard Development
- KPI Design and Visualization
- Business Decision-Making Using Data

---

## 🏆 Conclusion

This project demonstrates how Python-based analytics and Power BI dashboards can be combined to transform raw financial data into actionable business insights. By integrating stock performance, company fundamentals, volatility metrics, sector analysis, and market sentiment, the dashboard provides a comprehensive framework for investment evaluation and decision-making.

---

## Author

Shekhar Tanwar# Indian-Stock-Market-Analysis
Python and Power BI project analyzing Indian stocks using historical prices, fundamentals, and news sentiment
