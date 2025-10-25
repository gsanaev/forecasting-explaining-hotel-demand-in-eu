"""
merge_datasets.py
-----------------
Merges Eurostat (hotel demand, GDP, unemployment, turnover, HICP)
with OWID COVID, exchange rates, and policy stringency data.

⚙️ Clean version:
- No lag creation
- No imputation or zero-filling
- No time-range truncation
- Only merges and basic column alignment

Output → data/interim/hotel_panel.csv
"""

import pandas as pd
from pathlib import Path
import pycountry

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
RAW = Path("data/raw")
OUT = Path("data/interim/hotel_panel.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# HELPERS
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
# MAIN FUNCTION
# ---------------------------------------------------------------------
def merge_datasets():
    print("📥 Merging Eurostat, COVID, Exchange Rates, and Policy Stringency data...")

    # -----------------------------------------------------------------
    # EUROSTAT CORE
    # -----------------------------------------------------------------
    euro_path = RAW / "eurostat_hotels.csv"
    if not euro_path.exists():
        raise FileNotFoundError(f"❌ Missing file: {euro_path}")
    euro = load_csv(euro_path)
    euro["region"] = euro["region"].str.upper().str.strip()
    print(f"✅ Loaded Eurostat dataset → {len(euro):,} rows, {euro['region'].nunique()} countries")

    # -----------------------------------------------------------------
    # COVID CASES (OWID)
    # -----------------------------------------------------------------
    covid_path = RAW / "covid_cases.csv"
    if not covid_path.exists():
        print("⚠️ COVID dataset not found — proceeding without it.")
        covid = pd.DataFrame(columns=["region", "month", "covid_cases"])
    else:
        covid = load_csv(covid_path)
        if "iso3" in covid.columns:
            covid["region"] = covid["iso3"].apply(iso3_to_iso2).str.upper()
        covid = covid.rename(columns={"cases_per_100k": "covid_cases"})
        print(f"✅ Loaded COVID dataset → {len(covid):,} rows")

    # -----------------------------------------------------------------
    # MERGE EUROSTAT + COVID
    # -----------------------------------------------------------------
    merged = euro.merge(
        covid[["region", "month", "covid_cases"]],
        on=["region", "month"],
        how="left"
    )

    # ❌ Removed: filling NaNs and filtering date range
    print(f"✅ Initial merged shape: {merged.shape}")

    # -----------------------------------------------------------------
    # EXCHANGE RATES (Yahoo Finance)
    # -----------------------------------------------------------------
    exr_path = RAW / "exchange_rates.csv"
    if exr_path.exists():
        exr = pd.read_csv(exr_path)
        # Handle flexible date column name
        if "time" in exr.columns:
            exr["time"] = pd.to_datetime(exr["time"])
        elif "month" in exr.columns:
            exr = exr.rename(columns={"month": "time"})
            exr["time"] = pd.to_datetime(exr["time"])
        else:
            raise KeyError("❌ Exchange rates file missing time/month column.")

        exr["time"] = exr["time"].dt.to_period("M").dt.to_timestamp("M", "start")

        merged = merged.merge(exr, left_on="month", right_on="time", how="left")
        if "time" in merged.columns:
            merged = merged.drop(columns=["time"])
        print(f"✅ Exchange rates merged ({merged[['eurusd','eurgbp']].notna().mean().round(2)} non-null share)")
    else:
        print("⚠️ Exchange rates file not found; skipping merge.")

    # -----------------------------------------------------------------
    # POLICY STRINGENCY (Oxford COVID Tracker)
    # -----------------------------------------------------------------
    pol_path = RAW / "policy_stringency.csv"
    if pol_path.exists():
        stringency = pd.read_csv("data/raw/policy_stringency.csv", parse_dates=["month"])
        stringency["month"] = stringency["month"].dt.to_period("M").dt.to_timestamp("M", "start")
                        
        if "month" not in stringency.columns:
            stringency["month"] = stringency["time"].dt.to_period("M").dt.to_timestamp("M", "start")

        # Determine region column safely
        if "region" in stringency.columns:
            region_col = "region"
        elif "CountryCode" in stringency.columns:
            region_col = "CountryCode"
        else:
            raise KeyError("❌ Neither 'region' nor 'CountryCode' column found in policy stringency data.")

        # Map ISO3 → ISO2 for EU countries
        iso_map = {
            "AUT": "AT", "BEL": "BE", "BGR": "BG", "CYP": "CY", "CZE": "CZ", "DEU": "DE", "DNK": "DK", "EST": "EE",
            "ESP": "ES", "FIN": "FI", "FRA": "FR", "GRC": "GR", "HRV": "HR", "HUN": "HU", "IRL": "IE", "ITA": "IT",
            "LTU": "LT", "LUX": "LU", "LVA": "LV", "MLT": "MT", "NLD": "NL", "POL": "PL", "PRT": "PT", "ROU": "RO",
            "SWE": "SE", "SVN": "SI", "SVK": "SK"
        }
        stringency["region"] = stringency[region_col].map(iso_map)

        merged = merged.merge(stringency, on=["region", "month"], how="left")
        print(f"✅ Policy stringency merged ({merged['policy_stringency'].notna().mean():.2%} non-missing)")
    else:
        print("⚠️ Policy stringency file not found; skipping merge.")

    # -----------------------------------------------------------------
    # SAVE MERGED OUTPUT
    # -----------------------------------------------------------------
    merged.to_csv(OUT, index=False)
    print(f"💾 Saved merged dataset → {OUT.resolve()} ({len(merged):,} rows)")

    # -----------------------------------------------------------------
    # BASIC SUMMARY
    # -----------------------------------------------------------------
    if "month" in merged.columns:
        merged["year"] = merged["month"].dt.year
        cols = ["nights_spent", "gdp", "unemployment_rate", "turnover_index", "hicp_index", "covid_cases"]
        existing_cols = [c for c in cols if c in merged.columns]
        completeness = merged.groupby("year")[existing_cols].apply(lambda x: x.notna().mean().round(2))
        print("\n📊 Non-null share by year:")
        print(completeness.tail(10))


# ---------------------------------------------------------------------
if __name__ == "__main__":
    merge_datasets()
