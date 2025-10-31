# Safe SSL context setup (prevents CERTIFICATE_VERIFY_FAILED on some systems)
import ssl
import certifi

try:
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
except Exception:
    # Fallback (not ideal, but avoids crashes)
    ssl._create_default_https_context = ssl._create_unverified_context

from pathlib import Path
import pandas as pd
import pycountry

"""
policy_stringency_download.py
-----------------------------
Downloads Oxford COVID-19 Government Response Tracker (OxCGRT)
policy stringency index (0–100) and aggregates it to monthly MEAN values per country.

Output: data/raw/policy_stringency.csv
"""

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
OUT = Path("data/raw/policy_stringency.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

URL = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_nat_latest.csv"


# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main(force=False):
    if OUT.exists() and not force:
        print(f"✅ Using cached file → {OUT.resolve()}")
        return

    print("📥 Downloading Oxford COVID-19 Stringency Index data...")
    df = pd.read_csv(URL, low_memory=False)

    # Detect the correct stringency column
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

    # Parse and standardize dates
    df["Date"] = df["Date"].astype(str).str.zfill(8)  # Ensure YYYYMMDD
    df["date"] = pd.to_datetime(df["Date"], format="%Y%m%d", errors="coerce")
    df = df.dropna(subset=["date"])

    # Convert to monthly mean and align to first day of month
    # Represent month as YYYY-MM-DD string for first day of month
    df["month"] = df["date"].dt.to_period("M").astype(str) + "-01"

    monthly = (
        df.groupby(["CountryCode", "month"], as_index=False)
        .agg({"policy_stringency": "mean"})  # monthly mean of daily index
        .rename(columns={"CountryCode": "region"})
    )

    # Filter to EU only (ISO3)
    EU3 = [
        "AUT", "BEL", "BGR", "CYP", "CZE", "DEU", "DNK", "EST", "ESP", "FIN",
        "FRA", "GRC", "HRV", "HUN", "IRL", "ITA", "LTU", "LUX", "LVA", "MLT",
        "NLD", "POL", "PRT", "ROU", "SWE", "SVN", "SVK",
    ]
    monthly = monthly[monthly["region"].isin(EU3)]

    # ✅ Convert ISO3 → ISO2 for consistency with other datasets
    def iso3_to_iso2(iso3):
        try:
            # Guard against non-string and missing values
            if not isinstance(iso3, str) or not iso3:
                return None
            iso3_clean = iso3.strip().upper()

            # If already ISO2, return it
            if len(iso3_clean) == 2:
                return iso3_clean

            country = pycountry.countries.get(alpha_3=iso3_clean)
            if country and getattr(country, "alpha_2", None):
                return country.alpha_2

            return None
        except Exception:
            return None

    monthly["region"] = monthly["region"].apply(iso3_to_iso2)
    monthly = monthly.dropna(subset=["region"])

    # ✅ Keep data between 2015-01-01 and 2025-08-01 inclusive
    monthly = monthly[monthly["month"].between("2015-01-01", "2025-08-01")]

    # ✅ Sort and save
    monthly = monthly.sort_values(["region", "month"]).reset_index(drop=True)
    monthly.to_csv(OUT, index=False)

    print(f"💾 Saved → {OUT.resolve()} ({len(monthly):,} rows, {monthly['region'].nunique()} EU countries)")
    print(f"🗓️ Coverage: {monthly['month'].min()} → {monthly['month'].max()}")

    # Quick sanity check
    print("\n📊 Sample (2020):")
    print(monthly[monthly['month'].str.startswith('2020')].head())


# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
