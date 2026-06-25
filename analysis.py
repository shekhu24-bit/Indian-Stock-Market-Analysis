import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

stock_df = pd.read_csv("stock_prices.csv")
fund_df = pd.read_csv("company_fundamentals.csv")
news_df = pd.read_csv("news_sentiment.csv")

print("=" * 60)
print("INDIAN STOCK MARKET ANALYSIS REPORT")
print("=" * 60)

# ==========================================
# 1. AVERAGE CLOSING PRICE
# ==========================================

print("\n1. AVERAGE CLOSING PRICE")

avg_close = (
    stock_df
    .groupby("Company")["Close"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print(avg_close)

# ==========================================
# 2. HIGHEST STOCK PRICE
# ==========================================

print("\n2. HIGHEST STOCK PRICE")

highest_price = (
    stock_df
    .groupby("Company")["High"]
    .max()
    .round(2)
    .sort_values(ascending=False)
)

print(highest_price)

# ==========================================
# 3. LOWEST STOCK PRICE
# ==========================================

print("\n3. LOWEST STOCK PRICE")

lowest_price = (
    stock_df
    .groupby("Company")["Low"]
    .min()
    .round(2)
    .sort_values()
)

print(lowest_price)

# ==========================================
# 4. AVERAGE TRADING VOLUME
# ==========================================

print("\n4. AVERAGE TRADING VOLUME")

avg_volume = (
    stock_df
    .groupby("Company")["Volume"]
    .mean()
    .round(0)
    .sort_values(ascending=False)
)

print(avg_volume)

# ==========================================
# 5. VOLATILITY
# ==========================================
# Standard deviation of daily returns
# Higher volatility = Higher risk

print("\n5. VOLATILITY (Daily Returns Std Dev)")

stock_df["DailyReturn"] = (
    stock_df
    .groupby("Company")["Close"]
    .pct_change()
)

volatility = (
    stock_df
    .groupby("Company")["DailyReturn"]
    .std()
    .round(4)
    .sort_values()
)

print(volatility)
print("(Lower = Less Risky)")

# ==========================================
# 6. FUNDAMENTAL ANALYSIS
# ==========================================

print("\n6. FUNDAMENTAL ANALYSIS")

fundamentals = fund_df[
    [
        "Company",
        "Sector",
        "MarketCap",
        "PE_Ratio",
        "DividendYield"
    ]
]

print(fundamentals.to_string(index=False))

# ==========================================
# 7. SECTOR-WISE ANALYSIS
# ==========================================
# Compare average PE and Dividend by sector

print("\n7. SECTOR-WISE ANALYSIS")

sector_analysis = (
    fund_df
    .groupby("Sector")
    .agg(
        Avg_PE=("PE_Ratio", "mean"),
        Avg_Dividend=("DividendYield", "mean"),
        Companies=("Company", "count")
    )
    .round(2)
    .sort_values("Avg_PE")
)

print(sector_analysis)

# ==========================================
# 8. AVERAGE NEWS SENTIMENT
# ==========================================

print("\n8. AVERAGE NEWS SENTIMENT")

sentiment_scores = (
    news_df
    .groupby("Company")["SentimentScore"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print(sentiment_scores)

# ==========================================
# 9. NEWS DISTRIBUTION
# ==========================================

print("\n9. NEWS DISTRIBUTION")

sentiment_distribution = (
    news_df["Sentiment"]
    .value_counts()
)

print(sentiment_distribution)

# ==========================================
# 10. INVESTMENT SCORE
# ==========================================
# Formula:
# InvestmentScore = (Sentiment x 40) + (100 - PE_Ratio) + (DividendYield x 5)
# Sentiment     -> Market confidence (weight 40)
# PE_Ratio      -> Valuation (lower is better)
# DividendYield -> Passive income (weight 5)

print("\n10. INVESTMENT SCORE (IMPROVED FORMULA)")

sentiment_avg = (
    news_df
    .groupby("Company")["SentimentScore"]
    .mean()
)

ranking = fund_df.copy()

ranking["SentimentScore"] = ranking["Company"].map(
    sentiment_avg
)

ranking["Volatility"] = ranking["Company"].map(
    volatility
)

ranking["InvestmentScore"] = (
    ranking["SentimentScore"] * 40
    + (100 - ranking["PE_Ratio"])
    + ranking["DividendYield"] * 5
)

ranking = ranking.sort_values(
    by="InvestmentScore",
    ascending=False
).reset_index(drop=True)

ranking.index = ranking.index + 1

print(
    ranking[
        [
            "Company",
            "PE_Ratio",
            "DividendYield",
            "SentimentScore",
            "InvestmentScore"
        ]
    ].to_string()
)

# ==========================================
# 11. BEST INVESTMENT OPTION
# ==========================================

best_stock = ranking.iloc[0]

print("\n11. BEST INVESTMENT OPTION")

print(
    f"""
Company          : {best_stock['Company']}
Sector           : {best_stock['Sector']}
Investment Score : {best_stock['InvestmentScore']:.2f}
PE Ratio         : {best_stock['PE_Ratio']}
Dividend Yield   : {best_stock['DividendYield']}%
Avg Sentiment    : {best_stock['SentimentScore']:.2f}
Volatility       : {best_stock['Volatility']:.4f}
"""
)

# ==========================================
# 12. EXECUTIVE SUMMARY
# ==========================================

print("\n12. EXECUTIVE SUMMARY")

total_companies = len(fund_df)
total_records = len(stock_df)
total_news = len(news_df)
positive_pct = round(
    (news_df["Sentiment"] == "Positive").sum()
    / len(news_df) * 100,
    1
)

print(
    f"""
This analysis evaluated {total_companies} Indian companies
using {total_records} stock price records and
{total_news} news sentiment records.

Metrics evaluated:
  - Average Closing Price
  - Highest & Lowest Stock Price
  - Trading Volume
  - Daily Volatility (Risk)
  - Market Capitalization
  - PE Ratio
  - Dividend Yield
  - News Sentiment Score
  - Sector-wise Comparison

Overall news sentiment was {positive_pct}% positive.

Investment Score Formula:
  (Sentiment x 40) + (100 - PE Ratio) + (Dividend Yield x 5)

Best Investment: {best_stock['Company']}
Score: {best_stock['InvestmentScore']:.2f}
"""
)

print("\nREPORT COMPLETED")
print("=" * 60)