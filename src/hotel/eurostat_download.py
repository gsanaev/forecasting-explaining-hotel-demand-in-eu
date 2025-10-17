"""
eurostat_download.py — Eurostat downloader
Downloads EU-27 data for:
  - nights spent (tour_occ_nim)
  - air passengers (avia_tppa)
  - GDP (nama_10_gdp)
  - unemployment (une_rt_m)
Outputs tidy CSV with region, month, and indicators.
"""

from pathlib import Path
import pandas as pd
from eurostat import get_data_df

OUT = Path("data/raw/eurostat_hotels.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

EU = set("AT BE BG CY CZ DE DK EE ES FI FR GR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split())
GDP_F = {"na_item": ["B1GQ"], "unit": ["CLV10_MEUR"], "s_adj": ["NSA"]}
UNEMP_F = {"unit": ["PC_ACT"], "s_adj": ["NSA"]}


def _filter(df, filters=None):
    if df.empty:
        return df
    if "geo" in df.columns:
        df = df[df["geo"].str[:2].isin(EU)]
    if filters:
        for k, v in filters.items():
            if k in df.columns:
                df = df[df[k].isin(v)]
    return df


def _tidy(df, val):
    if df.empty:
        return pd.DataFrame(columns=["region", "month", val])
    geo = next((c for c in df.columns if "geo" in c.lower()), None)
    time = [c for c in df.columns if str(c)[:4].isdigit()]
    if not geo or not time:
        return pd.DataFrame(columns=["region", "month", val])
    df = df.melt(id_vars=[geo], value_vars=time, var_name="month", value_name=val)
    df = df.rename(columns={geo: "region"})
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df[val] = pd.to_numeric(df[val], errors="coerce")
    return df.dropna(subset=["month"])


def fetch(code, val, f=None, extra=None):
    try:
        df = get_data_df(code, flags=False)
    except Exception as e:
        print(f"⚠️ {code} failed: {e}")
        return pd.DataFrame(columns=["region", "month", val])
    df = _filter(df, f)
    if callable(extra):
        df = extra(df)
    return _tidy(df, val)


def main():
    print("📥 Downloading Eurostat datasets (compact mode)...")

    hotels = fetch("tour_occ_nim", "nights_spent")
    print(f"✅ Hotels: {len(hotels):,}")

    avia = fetch(
        "avia_tppa",
        "air_passengers",
        extra=lambda d: d[
            (d.get("tra_cov", "TOTAL").isin(["TOTAL", "INTL_XEU27_2020", "INTL"]))
            & (d.get("unit", "MIO_PKM") == "MIO_PKM")
            & (d.get("freq", "A") == "A")
        ],
    )
    print(f"✅ Air passengers: {len(avia):,}")

    gdp = fetch(
        "nama_10_gdp",
        "gdp",
        f=GDP_F,
        extra=lambda d: d[d.get("freq", "A") == "A"],
    )
    print(f"✅ GDP: {len(gdp):,}")

    unemp = fetch(
        "une_rt_m",
        "unemployment_rate",
        f=UNEMP_F,
        extra=lambda d: d[
            (d.get("sex", "T") == "T") & (d.get("age", "TOTAL") == "TOTAL")
        ],
    )
    print(f"✅ Unemployment: {len(unemp):,}")

    merged = (
        hotels.merge(avia, on=["region", "month"], how="left")
        .merge(gdp, on=["region", "month"], how="left")
        .merge(unemp, on=["region", "month"], how="left")
        .drop_duplicates(["region", "month"])
    )

    merged.to_csv(OUT, index=False)
    print(f"💾 Saved → {OUT.resolve()} ({len(merged):,} rows)")

    merged["year"] = merged["month"].dt.year
    cols = [c for c in ["nights_spent", "air_passengers", "gdp", "unemployment_rate"] if c in merged]
    print("\n📈 Data completeness:")
    print(merged.groupby("year")[cols].apply(lambda x: x.notna().mean().round(2)).tail(10))


if __name__ == "__main__":
    main()
