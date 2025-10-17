"""
clean_panel.py
--------------
Filters merged dataset (hotel_panel.csv) to analysis-ready subset:
- Keep only 2020–2022
- Drop countries without tourism data
- Ensure numeric types and consistent months
Outputs:
    data/processed/hotel_panel_clean.csv
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/processed/hotel_panel.csv")
OUT = Path("data/processed/hotel_panel_clean.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def clean_panel():
    print("🧹 Cleaning merged dataset...")

    df = pd.read_csv(RAW, parse_dates=["month"])
    df["year"] = df["month"].dt.year

    # Filter to COVID-era (2020–2022)
    df = df.query("2020 <= year <= 2022").copy()

    # Drop countries with no tourism data
    df = df[df["nights_spent"].notna()]

    # Optional: forward-fill small gaps within each country
    df = df.sort_values(["region", "month"])
    df[["stringency", "mobility_retail", "mobility_work"]] = (
        df.groupby("region")[["stringency", "mobility_retail", "mobility_work"]]
        .ffill()
        .bfill()
    )

    print(f"✅ Cleaned dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # Save clean version
    df.to_csv(OUT, index=False)
    print(f"💾 Saved cleaned dataset → {OUT.resolve()}")

    # Quick summary
    print("\n📊 Data coverage (non-null share):")
    print(df[["nights_spent", "stringency", "mobility_retail", "mobility_work"]].notna().mean().round(2))

    print("\n📈 Correlation matrix (2020–2022):")
    print(df[["nights_spent", "stringency", "mobility_retail", "mobility_work"]].corr().round(2))


if __name__ == "__main__":
    clean_panel()
