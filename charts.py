import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# LOAD DATA
# ==========================================

stock_df = pd.read_csv("stock_prices.csv")
fund_df = pd.read_csv("company_fundamentals.csv")
news_df = pd.read_csv("news_sentiment.csv")

# Charts folder create karo agar nahi hai
os.makedirs("charts", exist_ok=True)

# ==========================================
# CHART 1 — INVESTMENT SCORE
# ==========================================

sentiment_avg = (
    news_df
    .groupby("Company")["SentimentScore"]
    .mean()
)

ranking = fund_df.copy()

ranking["SentimentScore"] = ranking["Company"].map(
    sentiment_avg
)

ranking["InvestmentScore"] = (
    ranking["SentimentScore"] * 40
    + (100 - ranking["PE_Ratio"])
    + ranking["DividendYield"] * 5
)

ranking = ranking.sort_values(
    by="InvestmentScore",
    ascending=False
)

plt.figure(figsize=(12, 6))

plt.barh(
    ranking["Company"],
    ranking["InvestmentScore"],
    color="steelblue"
)

plt.xlabel("Investment Score")
plt.title("Investment Score Ranking — Indian Stocks")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("charts/investment_score.png")
plt.close()

print("Chart 1 saved — investment_score.png")

# ==========================================
# CHART 2 — NEWS SENTIMENT
# ==========================================

sentiment_scores = (
    news_df
    .groupby("Company")["SentimentScore"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))

plt.bar(
    sentiment_scores.index,
    sentiment_scores.values,
    color="mediumseagreen"
)

plt.xlabel("Company")
plt.ylabel("Avg Sentiment Score")
plt.title("Average News Sentiment — Indian Stocks")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("charts/sentiment_score.png")
plt.close()

print("Chart 2 saved — sentiment_score.png")

# ==========================================
# CHART 3 — PE RATIO vs DIVIDEND YIELD
# ==========================================

plt.figure(figsize=(10, 6))

plt.scatter(
    fund_df["PE_Ratio"],
    fund_df["DividendYield"],
    color="tomato",
    s=100
)

for i, row in fund_df.iterrows():
    plt.annotate(
        row["Company"],
        (row["PE_Ratio"], row["DividendYield"]),
        textcoords="offset points",
        xytext=(8, 4),
        fontsize=8
    )

plt.xlabel("PE Ratio")
plt.ylabel("Dividend Yield (%)")
plt.title("PE Ratio vs Dividend Yield")
plt.tight_layout()
plt.savefig("charts/pe_vs_dividend.png")
plt.close()

print("Chart 3 saved — pe_vs_dividend.png")

print("\nAll 3 charts saved in charts/ folder!")