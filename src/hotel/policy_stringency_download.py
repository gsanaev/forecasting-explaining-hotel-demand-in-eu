"""
policy_stringency_download.py
-----------------------------
Downloads Oxford COVID-19 Government Response Tracker (OxCGRT)
policy stringency index (0–100), keeps daily values, filters EU countries.

Output: data/raw/policy_stringency.csv
"""

from pathlib import Path
import pandas as pd

OUT = Path("data/raw/policy_stringency.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

URL = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_nat_latest.csv"

# EU ISO3 codes (consistent with Eurostat data)
EU3 = [
    "AUT","BEL","BGR","CYP","CZE","DEU","DNK","EST","ESP","FIN","FRA","GRC","HRV","HUN",
    "IRL","ITA","LTU","LUX","LVA","MLT","NLD","POL","PRT","ROU","SWE","SVN","SVK"
]


def main(force=False):
    if OUT.exists() and not force:
        print(f"✅ Using cached file → {OUT.resolve()}")
        return

    print("📥 Downloading Oxford COVID-19 Stringency Index data...")
    df = pd.read_csv(URL, low_memory=False)

    # Detect correct stringency column
    possible_cols = [
        "StringencyIndex",
        "StringencyIndex_Average",
        "StringencyIndex_ForDisplay",
        "StringencyIndex_Average_ForDisplay",
    ]
    str_col = next((c for c in possible_cols if c in df.columns), None)
    if not str_col:
        raise ValueError(f"No recognized stringency column found. Columns: {df.columns[:20].tolist()}")

    # Select relevant columns
    df = df[["CountryCode", "Date", str_col]].rename(columns={str_col: "policy_stringency"})

    # Parse date safely
    df["Date"] = df["Date"].astype(str).str.zfill(8)
    df["time"] = pd.to_datetime(df["Date"], format="%Y%m%d", errors="coerce")
    df = df.dropna(subset=["time"])

    # ✅ Filter to EU countries (safe, logical restriction)
    df = df[df["CountryCode"].isin(EU3)]

    # Save raw (daily, EU-only) dataset
    df.to_csv(OUT, index=False)
    print(f"💾 Saved → {OUT.resolve()} ({len(df):,} rows)")
    print(f"🗓️ Coverage: {df['time'].min().date()} → {df['time'].max().date()} | Countries: {df['CountryCode'].nunique()}")
    print(df.head(3))


if __name__ == "__main__":
    main()
