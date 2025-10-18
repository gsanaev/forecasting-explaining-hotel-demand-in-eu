"""
covid_cases_download.py
-----------------------
Downloads global COVID-19 case data (Our World in Data),
aggregates monthly totals per 100k population,
and saves a clean country-month CSV for merging.

Output:
    data/raw/covid_cases.csv
"""

import pandas as pd
from pathlib import Path
import requests
from io import StringIO

OUT = Path("data/raw/covid_cases.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def download_covid_cases():
    print("🦠 Downloading COVID-19 cases from Our World in Data...")

    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        df = pd.read_csv(
            StringIO(r.text),
            usecols=["iso_code", "location", "date", "new_cases", "population"]
        )
        print(f"✅ Successfully loaded data from {url}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to download OWID data: {e}")

    # --- Clean and aggregate ---
    df = df[df["iso_code"].str.len() == 3]  # keep ISO3 country codes only
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "population"])
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Cases per 100k population
    df["cases_per_100k"] = (df["new_cases"].fillna(0) / df["population"]) * 100_000

    # Monthly aggregation
    monthly = (
        df.groupby(["iso_code", "month"], as_index=False)
        .agg({"cases_per_100k": "sum"})
        .rename(columns={"iso_code": "iso3"})
    )

    # --- Fill pre-COVID and post-COVID periods with zeros ---
    # Create full grid (2000–2025 for all countries in data)
    months = pd.date_range("2000-01-01", "2025-12-01", freq="MS")
    countries = pd.Index(monthly["iso3"].unique())
    full_grid = pd.MultiIndex.from_product([countries, months], names=["iso3", "month"])
    monthly_full = (
        monthly.set_index(["iso3", "month"])
        .reindex(full_grid, fill_value=0)
        .reset_index()
    )

    # --- Save ---
    monthly_full.to_csv(OUT, index=False)
    print(f"💾 Saved {len(monthly_full):,} monthly records → {OUT.resolve()}")

    # --- Quick summary ---
    covid_years = monthly_full[monthly_full["month"].dt.year.between(2020, 2022)]
    print("\n📊 Summary (2020–2022):")
    print(covid_years.groupby("month")["cases_per_100k"].mean().head())

if __name__ == "__main__":
    download_covid_cases()
