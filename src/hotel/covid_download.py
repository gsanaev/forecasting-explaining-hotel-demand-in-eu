"""
covid_download.py
-----------------------
Downloads global COVID-19 case data (Our World in Data),
aggregates monthly totals per 100k population,
and saves an EU-only country-month CSV.

Output:
    data/raw/covid.csv
"""

import pandas as pd
from pathlib import Path
import requests
from io import StringIO
import pycountry  # for ISO3 → ISO2 conversion

OUT = Path("data/raw/covid.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def download_covid():
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
    df = df[df["iso_code"].str.len() == 3]  # only ISO3 country codes
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "population"])
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Cases per 100k population
    df["cases_per_100k"] = (df["new_cases"] / df["population"]) * 100_000

    # Monthly aggregation
    monthly = (
        df.groupby(["iso_code", "month"], as_index=False)
        .agg({"cases_per_100k": "sum"})
    )

    # --- EU countries (ISO3 codes) ---
    EU3 = [
        "AUT","BEL","BGR","CYP","CZE","DEU","DNK","EST","ESP","FIN","FRA","GRC","HRV","HUN",
        "IRL","ITA","LTU","LUX","LVA","MLT","NLD","POL","PRT","ROU","SWE","SVN","SVK"
    ]
    monthly = monthly[monthly["iso_code"].isin(EU3)]

    # --- Convert ISO3 → ISO2 and rename to 'region' ---
    def iso3_to_iso2(code: str) -> str | None:
        """Convert ISO3 country code to ISO2; return None if not found."""
        try:
            country = pycountry.countries.get(alpha_3=code)
            if country is not None:
                return country.alpha_2
            return None
        except Exception as _:
            # Optional: log or print(f"⚠️ Could not convert {code}: {e}")
            return None

    monthly["region"] = monthly["iso_code"].apply(iso3_to_iso2)

    # --- Select, reorder, and sort ---
    monthly = monthly[["month", "region", "cases_per_100k"]]
    monthly = monthly.sort_values(by=["region", "month"]).reset_index(drop=True)

    # --- Save ---
    monthly.to_csv(OUT, index=False)
    print(f"💾 Saved EU-only dataset → {OUT.resolve()} ({len(monthly):,} rows, {monthly['region'].nunique()} countries)")
    print("📆 Date range:", monthly['month'].min(), "→", monthly['month'].max())

if __name__ == "__main__":
    download_covid()
