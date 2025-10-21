"""
policy_stringency_download.py
-----------------------------
Downloads Oxford COVID-19 Government Response Tracker (OxCGRT)
policy stringency index (0–100) and aggregates it to monthly MEAN values per country.

Outputs: data/raw/policy_stringency.csv
"""

from pathlib import Path
import pandas as pd

OUT = Path("data/raw/policy_stringency.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

URL = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_nat_latest.csv"


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
    cols = ["CountryCode", "Date", str_col]
    df = df[cols].rename(columns={str_col: "policy_stringency"})

    # Parse date correctly
    df["Date"] = df["Date"].astype(str).str.zfill(8)  # ensure YYYYMMDD
    df["date"] = pd.to_datetime(df["Date"], format="%Y%m%d", errors="coerce")
    df = df.dropna(subset=["date"])

    # Convert to monthly mean
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp("M", "start")
    monthly = (
        df.groupby(["CountryCode", "month"], as_index=False)
        .agg({"policy_stringency": "mean"})  # 👈 monthly mean of daily index
        .rename(columns={"CountryCode": "region"})
    )

    # Filter to EU only (ISO3)
    EU3 = [
        "AUT","BEL","BGR","CYP","CZE","DEU","DNK","EST","ESP","FIN","FRA","GRC","HRV","HUN",
        "IRL","ITA","LTU","LUX","LVA","MLT","NLD","POL","PRT","ROU","SWE","SVN","SVK"
    ]
    monthly = monthly[monthly["region"].isin(EU3)]

    # Save
    monthly.to_csv(OUT, index=False)
    print(f"💾 Saved → {OUT.resolve()} ({len(monthly):,} rows, {monthly['region'].nunique()} EU countries)")
    print(f"🗓️ Coverage: {monthly['month'].min().date()} → {monthly['month'].max().date()}")

    # Quick sanity check
    print("\n📊 Sample (2020):")
    print(monthly[monthly['month'].dt.year == 2020].head())


if __name__ == "__main__":
    main()
