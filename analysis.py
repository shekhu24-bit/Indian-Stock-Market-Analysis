# ============================================================
# analysis.py
# Main analytical script — reads CSVs and prints insights
# Run after generate_dataset.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 60)
print("   Indian Stock Market — Analysis Report")
print("=" * 60)

# -------------------------------------------------------
# 1. Load Datasets
# -------------------------------------------------------
try:
    prices_df      = pd.read_csv("stock_prices.csv", parse_dates=["Date"])
    fundamentals_df = pd.read_csv("company_fundamentals.csv")
    sentiment_df   = pd.read_csv("news_sentiment.csv")
    print("\n✅ All datasets loaded successfully")
except FileNotFoundError as e:
    print(f"\n❌ Error: {e}")
    print("Please run generate_dataset.py first!")
    exit()

# -------------------------------------------------------
# 2. Basic Stats
# -------------------------------------------------------
print("\n" + "-" * 50)
print("📊 DATASET OVERVIEW")
print("-" * 50)
print(f"  Stock Price Records  : {len(prices_df):,}")
print(f"  Companies            : {prices_df['Company'].nunique()}")
print(f"  Date Range           : {prices_df['Date'].min().date()} to {prices_df['Date'].max().date()}")
print(f"  Fundamentals Records : {len(fundamentals_df)}")
print(f"  Sentiment Records    : {len(sentiment_df):,}")

# -------------------------------------------------------
# 3. Stock Performance Analysis
# -------------------------------------------------------
print("\n" + "-" * 50)
print("📈 STOCK PERFORMANCE — LAST 3 YEARS")
print("-" * 50)

performance = []
for company in prices_df["Company"].unique():
    df = prices_df[prices_df["Company"] == company].sort_values("Date")
    
    start_price = df["Close"].iloc[0]
    end_price   = df["Close"].iloc[-1]
    returns_pct = ((end_price - start_price) / start_price) * 100
    
    # Volatility — annualized standard deviation of daily returns
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    volatility = df["Daily_Return"].std() * np.sqrt(252) * 100  # Annualized %
    
    # Average Daily Volume
    avg_volume = df["Volume"].mean()
    
    # Max Drawdown
    rolling_max = df["Close"].cummax()
    drawdown    = (df["Close"] - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100
    
    performance.append({
        "Company":       company,
        "Start_Price":   round(start_price, 2),
        "End_Price":     round(end_price, 2),
        "Returns_%":     round(returns_pct, 2),
        "Volatility_%":  round(volatility, 2),
        "Max_Drawdown_%": round(max_drawdown, 2),
        "Avg_Volume":    int(avg_volume),
    })

perf_df = pd.DataFrame(performance).sort_values("Returns_%", ascending=False)

print(f"\n{'Company':<25} {'Returns %':>10} {'Volatility %':>13} {'Max Drawdown %':>15}")
print("-" * 65)
for _, row in perf_df.iterrows():
    print(f"{row['Company']:<25} {row['Returns_%']:>9.2f}% {row['Volatility_%']:>12.2f}% {row['Max_Drawdown_%']:>14.2f}%")

# -------------------------------------------------------
# 4. Fundamental Analysis
# -------------------------------------------------------
print("\n" + "-" * 50)
print("📋 FUNDAMENTAL ANALYSIS")
print("-" * 50)

print(f"\n{'Company':<25} {'PE Ratio':>10} {'Div Yield %':>12} {'ROE %':>8} {'Market Cap (₹T)':>16}")
print("-" * 75)
for _, row in fundamentals_df.iterrows():
    pe  = f"{row['PE_Ratio']:.1f}" if pd.notna(row.get("PE_Ratio")) else "N/A"
    dy  = f"{row['Dividend_Yield']:.2f}%" if pd.notna(row.get("Dividend_Yield")) else "N/A"
    roe = f"{row['ROE_Percent']:.1f}%" if pd.notna(row.get("ROE_Percent")) else "N/A"
    mc  = f"₹{row['Market_Cap_T']:.2f}T" if pd.notna(row.get("Market_Cap_T")) else "N/A"
    print(f"{row['Company']:<25} {pe:>10} {dy:>12} {roe:>8} {mc:>16}")

# -------------------------------------------------------
# 5. Sentiment Analysis
# -------------------------------------------------------
print("\n" + "-" * 50)
print("📰 SENTIMENT ANALYSIS")
print("-" * 50)

sent_summary = sentiment_df.groupby("Company").agg(
    Avg_Score  = ("Sentiment_Score", "mean"),
    Positive   = ("Sentiment", lambda x: (x == "Positive").sum()),
    Negative   = ("Sentiment", lambda x: (x == "Negative").sum()),
    Neutral    = ("Sentiment", lambda x: (x == "Neutral").sum()),
    Total      = ("Sentiment", "count")
).reset_index()

sent_summary["Positive_%"] = (sent_summary["Positive"] / sent_summary["Total"] * 100).round(1)
sent_summary = sent_summary.sort_values("Avg_Score", ascending=False)

print(f"\n{'Company':<25} {'Avg Score':>10} {'Positive %':>12} {'Negative':>9} {'Neutral':>8}")
print("-" * 68)
for _, row in sent_summary.iterrows():
    print(f"{row['Company']:<25} {row['Avg_Score']:>10.4f} {row['Positive_%']:>11.1f}% {row['Negative']:>9} {row['Neutral']:>8}")

overall_sentiment = sentiment_df["Sentiment_Score"].mean()
positive_pct = (sentiment_df["Sentiment"] == "Positive").sum() / len(sentiment_df) * 100
print(f"\n  Overall Market Sentiment Score : {overall_sentiment:.4f}")
print(f"  Overall Positive Coverage      : {positive_pct:.1f}%")

# -------------------------------------------------------
# 6. Improved Investment Score
# -------------------------------------------------------
print("\n" + "-" * 50)
print("🏆 INVESTMENT SCORE — RANKING")
print("-" * 50)
print("""
Investment Score Formula (Improved):
  = (Sentiment Score × 30)
  + (ROE % × 0.3)                ← Profitability
  + (Dividend Yield × 5)         ← Income
  + (1/PE_Ratio × 10)            ← Valuation (lower PE = better)
  - (Volatility % × 0.2)         ← Risk Penalty
""")

# Merge performance + fundamentals + sentiment
merged = perf_df.merge(fundamentals_df[["Company","PE_Ratio","Dividend_Yield","ROE_Percent"]], on="Company")
merged = merged.merge(sent_summary[["Company","Avg_Score"]], on="Company")

# Calculate score
def investment_score(row):
    score = 0
    score += row["Avg_Score"] * 30
    if pd.notna(row.get("ROE_Percent")):
        score += row["ROE_Percent"] * 0.3
    if pd.notna(row.get("Dividend_Yield")):
        score += row["Dividend_Yield"] * 5
    if pd.notna(row.get("PE_Ratio")) and row["PE_Ratio"] > 0:
        score += (1 / row["PE_Ratio"]) * 10
    score -= row["Volatility_%"] * 0.2
    return round(score, 2)

merged["Investment_Score"] = merged.apply(investment_score, axis=1)
merged = merged.sort_values("Investment_Score", ascending=False).reset_index(drop=True)
merged["Rank"] = merged.index + 1

print(f"\n{'Rank':<5} {'Company':<25} {'Score':>8} {'Returns %':>10} {'Volatility %':>13}")
print("-" * 65)
for _, row in merged.iterrows():
    print(f"{int(row['Rank']):<5} {row['Company']:<25} {row['Investment_Score']:>8.2f} {row['Returns_%']:>9.2f}% {row['Volatility_%']:>12.2f}%")

# -------------------------------------------------------
# 7. Sector Analysis
# -------------------------------------------------------
print("\n" + "-" * 50)
print("🏭 SECTOR-WISE ANALYSIS")
print("-" * 50)

sector_merged = merged.merge(fundamentals_df[["Company","Sector"]], on="Company")
sector_analysis = sector_merged.groupby("Sector").agg(
    Companies       = ("Company", "count"),
    Avg_Returns     = ("Returns_%", "mean"),
    Avg_Volatility  = ("Volatility_%", "mean"),
    Avg_PE          = ("PE_Ratio", "mean"),
    Avg_Score       = ("Investment_Score", "mean")
).reset_index().sort_values("Avg_Score", ascending=False)

print(f"\n{'Sector':<25} {'Companies':>10} {'Avg Return %':>13} {'Avg PE':>8} {'Avg Score':>10}")
print("-" * 70)
for _, row in sector_analysis.iterrows():
    pe = f"{row['Avg_PE']:.1f}" if pd.notna(row["Avg_PE"]) else "N/A"
    print(f"{row['Sector']:<25} {int(row['Companies']):>10} {row['Avg_Returns']:>12.2f}% {pe:>8} {row['Avg_Score']:>10.2f}")

# -------------------------------------------------------
# 8. Key Insights
# -------------------------------------------------------
print("\n" + "-" * 50)
print("🔍 KEY INSIGHTS")
print("-" * 50)

top_company   = merged.iloc[0]["Company"]
top_returner  = perf_df.iloc[0]["Company"]
top_sentiment = sent_summary.iloc[0]["Company"]
top_dividend  = fundamentals_df.sort_values("Dividend_Yield", ascending=False).iloc[0]
most_volatile = perf_df.sort_values("Volatility_%", ascending=False).iloc[0]["Company"]

print(f"""
  🥇 Top Investment Score  : {top_company}
  📈 Highest 3Y Returns    : {top_returner} ({perf_df.iloc[0]['Returns_%']:.2f}%)
  😊 Best Market Sentiment : {top_sentiment}
  💰 Highest Dividend Yield: {top_dividend['Company']} ({top_dividend['Dividend_Yield']:.2f}%)
  ⚠️  Most Volatile Stock   : {most_volatile}
  📊 Overall Market Sentiment: {'Positive' if overall_sentiment > 0 else 'Negative'} ({overall_sentiment:.4f})
""")

# Save final ranking to CSV
merged.to_csv("investment_ranking.csv", index=False)
print("✅ investment_ranking.csv saved!")

print("\n" + "=" * 60)
print("✅ Analysis Complete! Next: Run python charts.py")
print("=" * 60)