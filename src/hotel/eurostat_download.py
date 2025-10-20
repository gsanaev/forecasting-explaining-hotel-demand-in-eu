"""
eurostat_download.py
--------------------
Downloads long-term Eurostat datasets for the European hotel industry (raw 2015–2025+ data, unaltered).

Includes:
  - nights spent (tour_occ_nim)
  - GDP (namq_10_gdp quarterly, nama_10_gdp annual)
  - unemployment rate (une_rt_m)
  - turnover index (sts_setu_m)
  - HICP (prc_hicp_midx)
"""

from pathlib import Path
import pandas as pd
from eurostat import get_data_df
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
OUT = Path("data/raw/eurostat_hotels.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

EU = set("AT BE BG CY CZ DE DK EE ES FI FR GR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split())

UNEMP_F = {"unit": ["PC_ACT"], "s_adj": ["NSA"]}

# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------
def normalize_df(df):
    """Flatten MultiIndex and rename 'geo' column to 'region'."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join(c for c in col if c) for col in df.columns]
    df = df.reset_index(drop=False)
    geo_col = next((c for c in df.columns if "geo" in c.lower()), None)
    if not geo_col:
        return pd.DataFrame(columns=["region"])
    return df.rename(columns={geo_col: "region"})


def tidy(df, value_col):
    """Convert Eurostat wide format to tidy long format."""
    time_cols = [c for c in df.columns if any(x.isdigit() for x in str(c))]
    df = df.melt(id_vars=["region"], value_vars=time_cols, var_name="time", value_name=value_col)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    return df.dropna(subset=["time"])


def fetch_dataset(code, value_col, filters):
    """Generic Eurostat fetch and tidy"""
    try:
        raw = get_data_df(code, flags=False)
    except Exception as e:
        print(f"❌ Failed {code}: {e}")
        return pd.DataFrame(columns=["region", "time", value_col])
    df = normalize_df(raw)
    if df.empty:
        return df
    for k, v in filters.items():
        if k in df.columns:
            df = df[df[k].isin(v)]
    df = df[df["region"].str[:2].isin(EU)]
    return tidy(df, value_col)

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main():
    print("📥 Downloading Eurostat datasets...")

    # --- Nights spent ---
    hotels = fetch_dataset("tour_occ_nim", "nights_spent", {})
    print(f"✅ Hotels: {len(hotels):,}")

    # --- GDP: quarterly + fallback annual ---
    print("📊 Fetching GDP (quarterly + annual fallback)...")

    q_filters = {
        "na_item": ["B1G", "B1GQ"],
        "unit": ["CP_MEUR", "CLV05_MEUR", "CLV10_MEUR"],
        "s_adj": ["NSA", "CA"],
    }
    gdp_q = fetch_dataset("namq_10_gdp", "gdp", q_filters)

    # ❌ Removed: interpolation to monthly to preserve raw data
    if not gdp_q.empty:
        gdp_q = gdp_q.drop_duplicates(subset=["region", "time"])
        print(f"✅ Quarterly GDP: {len(gdp_q):,} rows")
    else:
        print("⚠️ Quarterly GDP missing, attempting annual fallback...")

    a_filters = {"na_item": ["B1G"], "unit": ["CLV10_MEUR"], "s_adj": ["NSA"]}
    gdp_a = fetch_dataset("nama_10_gdp", "gdp", a_filters)
    gdp = (
        pd.concat([gdp_q, gdp_a], ignore_index=True)
        .drop_duplicates(subset=["region", "time"], keep="first")
    )

    gdp["region"] = gdp["region"].str.upper().str.strip()
    gdp["time"] = gdp["time"].dt.to_period("M").dt.to_timestamp("M", "start")

    # --- Unemployment ---
    unemp = fetch_dataset("une_rt_m", "unemployment_rate", UNEMP_F)
    print(f"✅ Unemployment: {len(unemp):,}")

    # --- Turnover ---
    print("🏨 Fetching hospitality turnover index...")
    TURNOVER_F = {
        "indic_bt": ["NETTUR"],
        "nace_r2": ["I", "I55", "I56"],
        "s_adj": ["CA"],
        "unit": ["I21"],
    }
    turnover = fetch_dataset("sts_setu_m", "turnover_index", TURNOVER_F)
    print(f"✅ Turnover: {len(turnover):,}")

    # --- HICP ---
    print("💶 Fetching HICP (Harmonised Index of Consumer Prices)...")
    HICP_F = {
        "coicop": ["CP00"],
        "unit": ["I15", "I21"],
        "geo": list(EU),
    }
    hicp = fetch_dataset("prc_hicp_midx", "hicp_index", HICP_F)
    print(f"✅ HICP: {len(hicp):,}")

    # --- Align all to month start ---
    for df_ in [hotels, gdp, unemp, turnover, hicp]:
        if not df_.empty:
            df_["time"] = df_["time"].dt.to_period("M").dt.to_timestamp("M", "start")

    # --- Merge all ---
    merged = (
        hotels.merge(gdp, on=["region", "time"], how="left")
        .merge(unemp, on=["region", "time"], how="left")
        .merge(turnover, on=["region", "time"], how="left")
        .merge(hicp, on=["region", "time"], how="left")
        .drop_duplicates(["region", "time"])
    )

    # ✅ Keep only data from 2015-01-01 until today
    today = datetime.now().strftime("%Y-%m-%d")
    merged = merged[merged["time"].between("2015-01-01", today)]

    merged.to_csv(OUT, index=False)
    print(f"💾 Saved → {OUT.resolve()} ({len(merged):,} rows)")

    merged["year"] = merged["time"].dt.year
    cols = ["nights_spent", "gdp", "unemployment_rate", "turnover_index"]
    summary = merged.groupby("year")[cols].apply(lambda x: x.notna().mean().round(2))
    print("\n📊 Data completeness (share of non-null values):")
    print(summary.tail(10))


if __name__ == "__main__":
    main()
