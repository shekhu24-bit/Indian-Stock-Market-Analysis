# ============================================================
# charts.py
# Generates all charts for Power BI and README
# Run after analysis.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")

# Style
plt.rcParams["figure.facecolor"]  = "#0d1117"
plt.rcParams["axes.facecolor"]    = "#161b22"
plt.rcParams["axes.edgecolor"]    = "#30363d"
plt.rcParams["text.color"]        = "#c9d1d9"
plt.rcParams["axes.labelcolor"]   = "#c9d1d9"
plt.rcParams["xtick.color"]       = "#8b949e"
plt.rcParams["ytick.color"]       = "#8b949e"
plt.rcParams["grid.color"]        = "#21262d"
plt.rcParams["font.family"]       = "DejaVu Sans"

COLORS = ["#58a6ff","#3fb950","#ff7b72","#f78166",
          "#d2a8ff","#79c0ff","#56d364","#e3b341",
          "#ffa657","#ff6e40"]

print("=" * 60)
print("   Generating Charts...")
print("=" * 60)

# -------------------------------------------------------
# Load data
# -------------------------------------------------------
try:
    prices_df       = pd.read_csv("stock_prices.csv", parse_dates=["Date"])
    fundamentals_df = pd.read_csv("company_fundamentals.csv")
    sentiment_df    = pd.read_csv("news_sentiment.csv")
    ranking_df      = pd.read_csv("investment_ranking.csv")
    print("\n✅ Datasets loaded")
except FileNotFoundError as e:
    print(f"❌ {e} — Run generate_dataset.py and analysis.py first!")
    exit()

companies = prices_df["Company"].unique().tolist()

# -------------------------------------------------------
# Chart 1: Investment Score Ranking (Bar)
# -------------------------------------------------------
print("\n📊 Chart 1: Investment Score Ranking...")
fig, ax = plt.subplots(figsize=(12, 6))

df_sorted = ranking_df.sort_values("Investment_Score")
bars = ax.barh(df_sorted["Company"], df_sorted["Investment_Score"],
               color=COLORS[:len(df_sorted)], edgecolor="none", height=0.6)

for bar, val in zip(bars, df_sorted["Investment_Score"]):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f"{val:.2f}", va="center", fontsize=9, color="#c9d1d9")

ax.set_xlabel("Investment Score", fontsize=11)
ax.set_title("🏆 Investment Score Ranking — NSE Top 10 Companies",
             fontsize=13, fontweight="bold", pad=15, color="#f0f6fc")
ax.axvline(df_sorted["Investment_Score"].mean(), color="#f78166",
           linestyle="--", linewidth=1.5, label="Market Average")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("charts/investment_score.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("   ✅ charts/investment_score.png saved")

# -------------------------------------------------------
# Chart 2: Sentiment Score Comparison (Bar)
# -------------------------------------------------------
print("\n📊 Chart 2: Sentiment Score Comparison...")

sent_avg = (sentiment_df
            .groupby("Company")["Sentiment_Score"]
            .mean()
            .sort_values(ascending=False)
            .reset_index())

fig, ax = plt.subplots(figsize=(12, 6))
bar_colors = ["#3fb950" if s > 0 else "#ff7b72" for s in sent_avg["Sentiment_Score"]]
bars = ax.bar(sent_avg["Company"], sent_avg["Sentiment_Score"],
              color=bar_colors, edgecolor="none", width=0.6)

for bar, val in zip(bars, sent_avg["Sentiment_Score"]):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.005 if val >= 0 else bar.get_height() - 0.015,
            f"{val:.3f}", ha="center", fontsize=8, color="#c9d1d9")

ax.axhline(0, color="#8b949e", linewidth=0.8)
ax.set_ylabel("Average Sentiment Score", fontsize=11)
ax.set_title("📰 News Sentiment Score — Company Comparison",
             fontsize=13, fontweight="bold", pad=15, color="#f0f6fc")
ax.set_xticklabels(sent_avg["Company"], rotation=30, ha="right", fontsize=9)

pos_patch = mpatches.Patch(color="#3fb950", label="Positive")
neg_patch = mpatches.Patch(color="#ff7b72", label="Negative")
ax.legend(handles=[pos_patch, neg_patch], fontsize=9)

plt.tight_layout()
plt.savefig("charts/sentiment_score.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("   ✅ charts/sentiment_score.png saved")

# -------------------------------------------------------
# Chart 3: PE Ratio vs Dividend Yield (Scatter)
# -------------------------------------------------------
print("\n📊 Chart 3: PE vs Dividend Yield...")

fig, ax = plt.subplots(figsize=(10, 7))

for i, (_, row) in enumerate(fundamentals_df.iterrows()):
    if pd.notna(row.get("PE_Ratio")) and pd.notna(row.get("Dividend_Yield")):
        ax.scatter(row["PE_Ratio"], row["Dividend_Yield"],
                   color=COLORS[i % len(COLORS)], s=200, zorder=5,
                   edgecolors="white", linewidths=0.8)
        ax.annotate(row["Company"],
                    (row["PE_Ratio"], row["Dividend_Yield"]),
                    textcoords="offset points", xytext=(8, 5),
                    fontsize=8, color="#c9d1d9")

ax.set_xlabel("PE Ratio (Lower = Better Value)", fontsize=11)
ax.set_ylabel("Dividend Yield % (Higher = Better Income)", fontsize=11)
ax.set_title("📉 PE Ratio vs Dividend Yield — Valuation vs Income",
             fontsize=13, fontweight="bold", pad=15, color="#f0f6fc")
ax.grid(True, alpha=0.3)

# Quadrant labels
xlim = ax.get_xlim()
ylim = ax.get_ylim()
xmid = (xlim[0] + xlim[1]) / 2
ymid = (ylim[0] + ylim[1]) / 2
ax.axvline(xmid, color="#30363d", linewidth=1, linestyle=":")
ax.axhline(ymid, color="#30363d", linewidth=1, linestyle=":")
ax.text(xlim[0]+0.5, ylim[1]-0.1, "✅ Best Zone\n(Low PE, High Div)", fontsize=8, color="#3fb950")
ax.text(xlim[1]-5,   ylim[1]-0.1, "⚠️ Growth\n(High PE, High Div)", fontsize=8, color="#e3b341")

plt.tight_layout()
plt.savefig("charts/pe_vs_dividend.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("   ✅ charts/pe_vs_dividend.png saved")

# -------------------------------------------------------
# Chart 4: Stock Price Trends (Multi-line)
# -------------------------------------------------------
print("\n📊 Chart 4: Stock Price Trends (Normalized)...")

fig, ax = plt.subplots(figsize=(14, 7))

for i, company in enumerate(companies):
    df = prices_df[prices_df["Company"] == company].sort_values("Date")
    # Normalize to 100 base
    normalized = (df["Close"] / df["Close"].iloc[0]) * 100
    ax.plot(df["Date"], normalized, label=company,
            color=COLORS[i % len(COLORS)], linewidth=1.5, alpha=0.85)

ax.axhline(100, color="#8b949e", linewidth=1, linestyle="--", alpha=0.5)
ax.set_ylabel("Indexed Price (Base = 100)", fontsize=11)
ax.set_xlabel("Date", fontsize=11)
ax.set_title("📈 Stock Price Trends — Normalized (Base 100)",
             fontsize=13, fontweight="bold", pad=15, color="#f0f6fc")
ax.legend(fontsize=8, loc="upper left", ncol=2,
          facecolor="#161b22", edgecolor="#30363d")
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig("charts/price_trends.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("   ✅ charts/price_trends.png saved")

# -------------------------------------------------------
# Chart 5: 3-Year Returns Comparison (Bar)
# -------------------------------------------------------
print("\n📊 Chart 5: 3-Year Returns Comparison...")

returns_data = []
for company in companies:
    df = prices_df[prices_df["Company"] == company].sort_values("Date")
    ret = ((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100
    returns_data.append({"Company": company, "Returns_%": round(ret, 2)})

returns_df = pd.DataFrame(returns_data).sort_values("Returns_%", ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
bar_colors = ["#3fb950" if r >= 0 else "#ff7b72" for r in returns_df["Returns_%"]]
bars = ax.bar(returns_df["Company"], returns_df["Returns_%"],
              color=bar_colors, edgecolor="none", width=0.6)

for bar, val in zip(bars, returns_df["Returns_%"]):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5 if val >= 0 else bar.get_height() - 2,
            f"{val:.1f}%", ha="center", fontsize=9, color="#c9d1d9")

ax.axhline(0, color="#8b949e", linewidth=0.8)
ax.set_ylabel("3-Year Returns (%)", fontsize=11)
ax.set_title("📊 3-Year Returns Comparison — NSE Top 10",
             fontsize=13, fontweight="bold", pad=15, color="#f0f6fc")
ax.set_xticklabels(returns_df["Company"], rotation=30, ha="right", fontsize=9)
ax.grid(True, alpha=0.2, axis="y")

plt.tight_layout()
plt.savefig("charts/returns_comparison.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("   ✅ charts/returns_comparison.png saved")

# -------------------------------------------------------
# Chart 6: Volatility (Risk) Comparison
# -------------------------------------------------------
print("\n📊 Chart 6: Volatility/Risk Comparison...")

vol_data = []
for company in companies:
    df = prices_df[prices_df["Company"] == company].sort_values("Date").copy()
    df["Daily_Return"] = df["Close"].pct_change()
    vol = df["Daily_Return"].std() * np.sqrt(252) * 100
    vol_data.append({"Company": company, "Volatility_%": round(vol, 2)})

vol_df = pd.DataFrame(vol_data).sort_values("Volatility_%", ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
vol_colors = plt.cm.RdYlGn_r(
    np.linspace(0.1, 0.9, len(vol_df))
)
bars = ax.bar(vol_df["Company"], vol_df["Volatility_%"],
              color=vol_colors, edgecolor="none", width=0.6)

for bar, val in zip(bars, vol_df["Volatility_%"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{val:.1f}%", ha="center", fontsize=9, color="#c9d1d9")

ax.set_ylabel("Annualized Volatility (%)", fontsize=11)
ax.set_title("⚠️ Annualized Volatility (Risk) — NSE Top 10",
             fontsize=13, fontweight="bold", pad=15, color="#f0f6fc")
ax.set_xticklabels(vol_df["Company"], rotation=30, ha="right", fontsize=9)
ax.grid(True, alpha=0.2, axis="y")

plt.tight_layout()
plt.savefig("charts/volatility.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("   ✅ charts/volatility.png saved")

# -------------------------------------------------------
# Done
# -------------------------------------------------------
print("\n" + "=" * 60)
print("✅ All 6 charts generated in /charts folder!")
print("=" * 60)
print("\nCharts created:")
print("  📊 investment_score.png    — Investment Ranking")
print("  📊 sentiment_score.png     — Sentiment Comparison")
print("  📊 pe_vs_dividend.png      — PE vs Dividend Scatter")
print("  📊 price_trends.png        — Normalized Price Trends")
print("  📊 returns_comparison.png  — 3-Year Returns")
print("  📊 volatility.png          — Risk/Volatility Comparison")
print("\nNext step: Open dashboard.pbix in Power BI Desktop → Refresh")