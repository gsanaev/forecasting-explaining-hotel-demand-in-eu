"""
hotel_merge.py
-----------------
Merges Eurostat (hotel demand, GDP, unemployment, turnover, HICP)
with OWID COVID, exchange rates, and policy stringency data.

✅ Clean 2025 version:
- All datasets aligned on region (ISO2) and month (YYYY-MM-DD)
- Robust to missing 'region' columns (e.g., FX rates)
- Sorted, validated, and ready for modeling

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

    # Check for 'month' column
    if "month" not in df.columns:
        raise KeyError(f"❌ {name} missing 'month' column")

    # Normalize month format
    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Normalize region codes if available
    if "region" in df.columns:
        df["region"] = df["region"].astype(str).str.upper().str.strip()
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

    # --- Load datasets ---
    euro = load_dataset("eurostat")
    covid = load_dataset("covid")
    fx = load_dataset("fx_rates")
    policy = load_dataset("policy_stringency")

    if euro.empty:
        raise FileNotFoundError("Eurostat data is required as the base dataset.")

    # --- Harmonize COVID column naming ---
    if not covid.empty and "cases_per_100k" in covid.columns:
        covid = covid.rename(columns={"cases_per_100k": "covid_cases"})

    # --- Merge step-by-step ---
    merged = euro.copy()

    # COVID
    if not covid.empty:
        merged = merged.merge(
            covid[["region", "month", "covid_cases"]],
            on=["region", "month"],
            how="left",
        )

    # FX rates (no region)
    if not fx.empty:
        fx = fx.rename(columns={"time": "month"}) if "time" in fx.columns else fx
        merged = merged.merge(fx[["month", "eurusd", "eurgbp"]], on="month", how="left")

    # Policy Stringency
    if not policy.empty:
        merged = merged.merge(
            policy[["region", "month", "policy_stringency"]],
            on=["region", "month"],
            how="left",
        )

    # --- Sort and clean ---
    merged = merged.drop_duplicates(["region", "month"]).sort_values(["region", "month"])
    merged.reset_index(drop=True, inplace=True)

    # --- Save ---
    merged.to_csv(OUT, index=False)
    print(f"💾 Saved merged dataset → {OUT.resolve()} ({len(merged):,} rows)")

    # --- Validation checks ---
    print("\n🔍 Validating dataset consistency...")

    # 1️⃣ Monotonic month order per country
    try:
        grouped = merged.groupby("region")["month"].apply(lambda x: x.is_monotonic_increasing)
        if not grouped.all():
            bad = grouped[~grouped].index.tolist()
            print(f"⚠️ Non-monotonic month order detected for: {bad}")
        else:
            print("✅ All countries have monotonic month sequence.")
    except Exception as e:
        print(f"⚠️ Could not validate month order: {e}")

    # 2️⃣ Completeness summary
    merged["year"] = pd.to_datetime(merged["month"]).dt.year
    cols = [
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
    available = [c for c in cols if c in merged.columns]
    completeness = merged.groupby("year")[available].apply(lambda x: x.notna().mean().round(2))

    print("\n📊 Non-null share by year:")
    print(completeness.tail(10))


# ---------------------------------------------------------------------
if __name__ == "__main__":
    merge_datasets()
