"""
merge_datasets.py
Merges Eurostat (hotel demand), OxCGRT (stringency), and Google Mobility data
into one monthly country-level panel.

Output → data/processed/hotel_panel.csv
"""

import pandas as pd
from pathlib import Path
import pycountry

OUT = Path("data/processed/hotel_panel.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)


def iso3_to_iso2(x):
    try:
        c = pycountry.countries.get(alpha_3=x)
        return c.alpha_2 if c else None
    except Exception:
        return None


def load_csv(path, date_col="month"):
    df = pd.read_csv(path)
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    return df


def merge_datasets():
    print("📥 Merging Eurostat, OxCGRT, and Mobility data...")

    euro = load_csv("data/raw/eurostat_hotels.csv")
    euro["region"] = euro["region"].str.upper().str.strip()

    oxcg = load_csv("data/raw/oxcgrt.csv")
    oxcg = oxcg.rename(columns={"CountryCode": "iso3", "StringencyIndex_Average": "stringency"})
    oxcg["region"] = oxcg["iso3"].apply(iso3_to_iso2).str.upper()

    mob = load_csv("data/raw/mobility_reports.csv")
    mob = mob.rename(columns={"country_region_code": "region"})
    mob["region"] = mob["region"].str.upper().str.strip()

    df = euro.merge(oxcg, on=["region", "month"], how="left").merge(mob, on=["region", "month"], how="left")
    print(f"✅ Final shape: {df.shape}")

    df.to_csv(OUT, index=False)
    print(f"💾 Saved merged dataset → {OUT.resolve()}")

    # Validation summary
    df["year"] = df["month"].dt.year
    cov = df.groupby("year")[["stringency", "mobility_retail", "mobility_work"]].apply(lambda x: x.notna().mean().round(2))
    print("\n📊 Non-null share by year:\n", cov.tail(10))

    recent = df[df["year"] >= 2020][["nights_spent", "stringency", "mobility_retail", "mobility_work"]]
    print("\n📈 Correlation matrix (2020+):\n", recent.corr().round(2))


if __name__ == "__main__":
    merge_datasets()
