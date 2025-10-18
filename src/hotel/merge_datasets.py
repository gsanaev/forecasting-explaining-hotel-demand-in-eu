"""
merge_datasets.py
-----------------
Merges Eurostat (hotel demand, GDP, unemployment, air traffic, turnover)
and OWID COVID case data into one monthly country-level panel (2015–2025).

Adds lagged variables (1–3 months) for GDP, unemployment, turnover, and COVID.

Output → data/processed/hotel_panel.csv
"""

import pandas as pd
from pathlib import Path
import pycountry

RAW = Path("data/raw")
OUT = Path("data/processed/hotel_panel.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def iso3_to_iso2(x: str):
    """Convert ISO3 → ISO2 codes."""
    try:
        c = pycountry.countries.get(alpha_3=x)
        return c.alpha_2 if c else None
    except Exception:
        return None


def load_csv(path: Path, date_col_candidates=("month", "time", "date")):
    """Load CSV and detect a suitable time column automatically."""
    df = pd.read_csv(path)

    # Try to detect a date/time column dynamically
    date_col = next((c for c in date_col_candidates if c in df.columns), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df["month"] = df[date_col].dt.to_period("M").dt.to_timestamp("M", "start")
    else:
        print(f"⚠️ No date column found in {path.name}. Columns: {df.columns.tolist()}")
    return df


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def merge_datasets():
    print("📥 Merging Eurostat macro data with COVID cases (2015–2025)...")

    # --- Eurostat core ---
    euro_path = RAW / "eurostat_hotels.csv"
    if not euro_path.exists():
        raise FileNotFoundError(f"❌ Missing file: {euro_path}")
    euro = load_csv(euro_path)
    euro["region"] = euro["region"].str.upper().str.strip()
    print(f"✅ Loaded Eurostat dataset → {len(euro):,} rows, {euro['region'].nunique()} countries")

    # --- COVID data ---
    covid_path = RAW / "covid_cases.csv"
    if not covid_path.exists():
        print("⚠️ COVID dataset not found — proceeding without it.")
        covid = pd.DataFrame(columns=["region", "month", "covid_cases"])
    else:
        covid = load_csv(covid_path)
        if "iso3" in covid.columns:
            covid["region"] = covid["iso3"].apply(iso3_to_iso2).str.upper()
        covid = covid.rename(columns={"cases_per_100k": "covid_cases"})
        print(f"✅ Loaded COVID dataset → {len(covid):,} rows, columns: {covid.columns.tolist()}")

    # --- Validate keys ---
    if "month" not in covid.columns:
        raise KeyError("❌ COVID dataset missing 'month' column after loading — check date column names.")
    if "month" not in euro.columns:
        raise KeyError("❌ Eurostat dataset missing 'month' column after loading.")

    # --- Merge ---
    merged = euro.merge(
        covid[["region", "month", "covid_cases"]],
        on=["region", "month"],
        how="left"
    )

    merged["covid_cases"] = merged["covid_cases"].fillna(0)
    merged = merged[merged["month"].between("2015-01-01", "2025-12-31")]

    # -----------------------------------------------------------------
    # 🕒 Add lagged variables (1–3 months)
    # -----------------------------------------------------------------
    print("🧩 Creating lagged variables (1–3 months)...")
    lag_cols = ["gdp", "turnover_index", "covid_cases", "unemployment_rate"]
    merged = merged.sort_values(["region", "month"])
    for col in lag_cols:
        if col in merged.columns:
            for lag in [1, 2, 3]:
                merged[f"{col}_lag{lag}"] = merged.groupby("region")[col].shift(lag)
    print(f"✅ Added lagged columns: {[f'{c}_lag1..3' for c in lag_cols if c in merged.columns]}")

    print(f"✅ Final merged shape: {merged.shape}")

    # --- Save ---
    merged.to_csv(OUT, index=False)
    print(f"💾 Saved merged dataset → {OUT.resolve()}")

    # --- Summary ---
    merged["year"] = merged["month"].dt.year
    cols = ["nights_spent", "gdp", "unemployment_rate", "turnover_index", "covid_cases"]
    existing_cols = [c for c in cols if c in merged.columns]

    completeness = merged.groupby("year")[existing_cols].apply(lambda x: x.notna().mean().round(2))
    print("\n📊 Non-null share by year:")
    print(completeness.tail(10))

    if {"gdp", "nights_spent", "covid_cases"}.issubset(merged.columns):
        recent = merged[merged["year"].between(2020, 2022)][existing_cols]
        print("\n📈 Correlation matrix (2020–2022):")
        print(recent.corr().round(2))


# ---------------------------------------------------------------------
if __name__ == "__main__":
    merge_datasets()
