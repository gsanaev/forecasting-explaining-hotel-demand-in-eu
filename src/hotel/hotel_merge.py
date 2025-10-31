"""
hotel_merge.py
-----------------
Merges Eurostat (hotel demand, GDP, unemployment, turnover, HICP)
with OWID COVID, exchange rates, and policy stringency data.

⚙️ Clean, harmonized version (2025)
- All datasets aligned on region (ISO2) and month (YYYY-MM-DD)
- No transformations or imputations
- Sorted and validated output

Output → data/interim/hotel.csv
"""

import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
RAW = Path("data/raw")
OUT = Path("data/interim/hotel.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------
def load_dataset(name: str) -> pd.DataFrame:
    """Load dataset safely from /data/raw/ and check expected columns."""
    path = RAW / f"{name}.csv"
    if not path.exists():
        print(f"⚠️ {name} not found → skipping merge.")
        return pd.DataFrame()

    df = pd.read_csv(path)
    if "month" not in df.columns:
        raise KeyError(f"❌ {name} missing 'month' column")

    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.strftime("%Y-%m-%d")

    if "region" in df.columns:
        df["region"] = df["region"].str.upper().str.strip()
        region_info = f"{df['region'].nunique()} countries"
    else:
        region_info = "no region column"

    print(f"✅ Loaded {name:<18} → {len(df):>7,} rows | {region_info}")
    return df

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def merge_datasets():
    print("📥 Merging Eurostat, COVID, FX rates, and Policy Stringency datasets...")

    # --- Load each dataset ---
    euro = load_dataset("eurostat")
    covid = load_dataset("covid")
    fx = load_dataset("fx_rates")
    policy = load_dataset("policy_stringency")

    if euro.empty:
        raise FileNotFoundError("Eurostat data is required as the base.")

    # --- Harmonize column names for clarity ---
    if "cases_per_100k" in covid.columns:
        covid = covid.rename(columns={"cases_per_100k": "covid_cases"})

    # --- Merge all datasets on (region, month) ---
    merged = euro.copy()
    merged = merged.merge(
        covid[["region", "month", "covid_cases"]],
        on=["region", "month"],
        how="left",
    )

    if not fx.empty:
        merged = merged.merge(fx[["month", "eurusd", "eurgbp"]], on="month", how="left")

    if not policy.empty:
        merged = merged.merge(
            policy[["region", "month", "policy_stringency"]],
            on=["region", "month"],
            how="left",
        )

    # --- Final formatting ---
    merged = merged.drop_duplicates(["region", "month"]).sort_values(["region", "month"])
    merged.reset_index(drop=True, inplace=True)

    # --- Save output ---
    merged.to_csv(OUT, index=False)
    print(f"💾 Saved merged dataset → {OUT.resolve()} ({len(merged):,} rows)")

    # --- Quick data completeness summary ---
    merged["year"] = pd.to_datetime(merged["month"]).dt.year
    summary_cols = [
        "nights_spent",
        "gdp",
        "unemployment_rate",
        "turnover_index",
        "hicp_index",
        "covid_cases",
        "eurusd",
        "eurgbp",
        "policy_stringency",
    ]
    existing = [c for c in summary_cols if c in merged.columns]
    completeness = merged.groupby("year")[existing].apply(lambda x: x.notna().mean().round(2))
    print("\n📊 Non-null share by year:")
    print(completeness.tail(10))

    assert merged.groupby("region")["month"].is_monotonic_increasing.all()

# ---------------------------------------------------------------------
if __name__ == "__main__":
    merge_datasets()
