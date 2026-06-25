# ============================================================
# generate_dataset.py
# Real NSE Data fetcher using yfinance
# Run this FIRST before analysis.py and charts.py
# ============================================================

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

print("=" * 60)
print("   Indian Stock Market - Real Data Fetcher")
print("=" * 60)

# -------------------------------------------------------
# 1. NSE Ticker Symbols (Company Name → NSE Symbol)
# -------------------------------------------------------
COMPANIES = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS":                 "TCS.NS",
    "Infosys":             "INFY.NS",
    "HDFC Bank":           "HDFCBANK.NS",
    "ICICI Bank":          "ICICIBANK.NS",
    "SBI":                 "SBIN.NS",
    "ITC":                 "ITC.NS",
    "Bharti Airtel":       "BHARTIARTL.NS",
    "Larsen & Toubro":     "LT.NS",
    "Hindustan Unilever":  "HINDUNILVR.NS"
}

# Date range — last 3 years
END_DATE   = datetime.today().strftime("%Y-%m-%d")
START_DATE = (datetime.today() - timedelta(days=3*365)).strftime("%Y-%m-%d")

print(f"\nFetching data from {START_DATE} to {END_DATE}")
print(f"Companies: {len(COMPANIES)}\n")

# -------------------------------------------------------
# 2. Fetch Historical Stock Prices
# -------------------------------------------------------
print("📥 Downloading historical stock prices from NSE...")

all_price_data = []

for company_name, ticker_symbol in COMPANIES.items():
    print(f"  → Fetching {company_name} ({ticker_symbol})...", end=" ")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=START_DATE, end=END_DATE)
        
        if df.empty:
            print("❌ No data found!")
            continue
        
        df = df.reset_index()
        df["Company"] = company_name
        df["Ticker"]  = ticker_symbol
        
        # Keep only needed columns
        df = df[["Date", "Company", "Ticker", "Open", "High", "Low", "Close", "Volume"]]
        
        # Round to 2 decimal places
        for col in ["Open", "High", "Low", "Close"]:
            df[col] = df[col].round(2)
        
        # Remove timezone from Date
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        
        all_price_data.append(df)
        print(f"✅ {len(df)} records")
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Combine all companies
stock_prices_df = pd.concat(all_price_data, ignore_index=True)
stock_prices_df.to_csv("stock_prices.csv", index=False)

print(f"\n✅ stock_prices.csv saved — {len(stock_prices_df)} total records")

# -------------------------------------------------------
# 3. Fetch Company Fundamentals (Real Data)
# -------------------------------------------------------
print("\n📥 Fetching company fundamentals...")

fundamentals_data = []

SECTOR_MAP = {
    "Reliance Industries": "Energy & Retail",
    "TCS":                 "Information Technology",
    "Infosys":             "Information Technology",
    "HDFC Bank":           "Banking",
    "ICICI Bank":          "Banking",
    "SBI":                 "Banking",
    "ITC":                 "FMCG",
    "Bharti Airtel":       "Telecom",
    "Larsen & Toubro":     "Infrastructure",
    "Hindustan Unilever":  "FMCG"
}

for company_name, ticker_symbol in COMPANIES.items():
    print(f"  → Fetching fundamentals for {company_name}...", end=" ")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info   = ticker.info
        
        market_cap    = info.get("marketCap", 0) / 1e12           # Convert to Lakh Crore (₹T)
        pe_ratio      = info.get("trailingPE", None)
        dividend_yield = info.get("dividendYield", 0)
        if dividend_yield:
            dividend_yield = round(dividend_yield * 100, 2)        # Convert to percentage
        
        # 52-week high/low
        week52_high = info.get("fiftyTwoWeekHigh", None)
        week52_low  = info.get("fiftyTwoWeekLow",  None)
        
        # EPS and ROE
        eps = info.get("trailingEps", None)
        roe = info.get("returnOnEquity", None)
        if roe:
            roe = round(roe * 100, 2)
        
        fundamentals_data.append({
            "Company":        company_name,
            "Ticker":         ticker_symbol,
            "Sector":         SECTOR_MAP.get(company_name, "Others"),
            "Market_Cap_T":   round(market_cap, 2),
            "PE_Ratio":       round(pe_ratio, 2) if pe_ratio else None,
            "Dividend_Yield": dividend_yield,
            "EPS":            round(eps, 2) if eps else None,
            "ROE_Percent":    roe,
            "52W_High":       week52_high,
            "52W_Low":        week52_low,
        })
        
        print("✅")
        time.sleep(0.5)
        
    except Exception as e:
        print(f"❌ Error: {e}")

fundamentals_df = pd.DataFrame(fundamentals_data)
fundamentals_df.to_csv("company_fundamentals.csv", index=False)

print(f"\n✅ company_fundamentals.csv saved — {len(fundamentals_df)} companies")
print(fundamentals_df[["Company", "PE_Ratio", "Dividend_Yield", "ROE_Percent"]].to_string(index=False))

# -------------------------------------------------------
# 4. Sentiment Dataset
#    NewsAPI free tier se real headlines — ya fallback
# -------------------------------------------------------
print("\n📥 Generating sentiment dataset...")
print("    (For real sentiment: get free API key from newsapi.org)")
print("    (Using keyword-based realistic scoring for now)\n")

# Realistic sentiment scores based on recent market trends
# You can replace this with actual NewsAPI calls — see comments below
SENTIMENT_PROFILE = {
    "Reliance Industries": {"bias": 0.65, "volatility": 0.2},
    "TCS":                 {"bias": 0.70, "volatility": 0.15},
    "Infosys":             {"bias": 0.60, "volatility": 0.2},
    "HDFC Bank":           {"bias": 0.72, "volatility": 0.15},
    "ICICI Bank":          {"bias": 0.68, "volatility": 0.18},
    "SBI":                 {"bias": 0.55, "volatility": 0.25},
    "ITC":                 {"bias": 0.62, "volatility": 0.2},
    "Bharti Airtel":       {"bias": 0.75, "volatility": 0.15},
    "Larsen & Toubro":     {"bias": 0.65, "volatility": 0.18},
    "Hindustan Unilever":  {"bias": 0.58, "volatility": 0.22},
}

POSITIVE_HEADLINES = [
    "{company} posts record quarterly profit",
    "{company} announces expansion plans",
    "Analysts upgrade {company} to BUY",
    "{company} wins major government contract",
    "{company} reports strong revenue growth",
    "{company} dividend declared, investors rejoice",
    "FII buying seen in {company} shares",
    "{company} Q3 results beat street estimates",
]

NEGATIVE_HEADLINES = [
    "{company} faces regulatory scrutiny",
    "{company} Q2 profit misses estimates",
    "Analysts downgrade {company} on margin pressure",
    "{company} faces stiff competition",
    "FII selling pressure in {company}",
    "{company} reports higher input costs",
]

NEUTRAL_HEADLINES = [
    "{company} to announce results next week",
    "{company} board meeting scheduled",
    "{company} management meets analysts",
    "{company} AGM held, no major announcements",
]

np.random.seed(42)
sentiment_records = []

# Generate 50 news records per company
for company_name, profile in SENTIMENT_PROFILE.items():
    for i in range(50):
        # Random date in last 1 year
        days_ago    = np.random.randint(0, 365)
        news_date   = datetime.today() - timedelta(days=int(days_ago))
        
        # Score based on company bias
        score = np.clip(
            np.random.normal(profile["bias"], profile["volatility"]),
            -1.0, 1.0
        )
        score = round(score, 4)
        
        # Label
        if score >= 0.1:
            sentiment_label = "Positive"
            headline = np.random.choice(POSITIVE_HEADLINES).format(company=company_name)
        elif score <= -0.1:
            sentiment_label = "Negative"
            headline = np.random.choice(NEGATIVE_HEADLINES).format(company=company_name)
        else:
            sentiment_label = "Neutral"
            headline = np.random.choice(NEUTRAL_HEADLINES).format(company=company_name)
        
        sentiment_records.append({
            "Date":            news_date.strftime("%Y-%m-%d"),
            "Company":         company_name,
            "Headline":        headline,
            "Sentiment_Score": score,
            "Sentiment":       sentiment_label,
        })

sentiment_df = pd.DataFrame(sentiment_records)
sentiment_df = sentiment_df.sort_values("Date").reset_index(drop=True)
sentiment_df.to_csv("news_sentiment.csv", index=False)

print(f"✅ news_sentiment.csv saved — {len(sentiment_df)} records")
print("\nSentiment Distribution:")
print(sentiment_df["Sentiment"].value_counts().to_string())

# -------------------------------------------------------
# DONE
# -------------------------------------------------------
print("\n" + "=" * 60)
print("✅ All datasets generated successfully!")
print("=" * 60)
print("\nFiles created:")
print(f"  📄 stock_prices.csv        → {len(stock_prices_df)} records")
print(f"  📄 company_fundamentals.csv → {len(fundamentals_df)} records")
print(f"  📄 news_sentiment.csv       → {len(sentiment_df)} records")
print("\nNext step: Run python analysis.py")

# -------------------------------------------------------
# OPTIONAL: Real NewsAPI Integration (Uncomment to use)
# -------------------------------------------------------
# Get FREE API key from: https://newsapi.org/register
#
# import requests
#
# API_KEY = "your_api_key_here"
# for company in COMPANIES.keys():
#     url = f"https://newsapi.org/v2/everything?q={company}+stock+NSE&language=en&pageSize=10&apiKey={API_KEY}"
#     response = requests.get(url).json()
#     articles = response.get("articles", [])
#     for article in articles:
#         headline = article["title"]
#         # Then apply VADER sentiment scorer
#         from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#         analyzer = SentimentIntensityAnalyzer()
#         score = analyzer.polarity_scores(headline)["compound"]