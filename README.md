# 🏨 Machine Learning Analysis of Hotel Demand Recovery in Europe After COVID-19

### 📘 Overview
This project analyzes how the European hotel industry has recovered following the COVID-19 pandemic using **econometric** and **machine learning** methods.  
It builds a harmonized Eurostat-based **monthly panel** (2015–2025) enriched with macroeconomic, COVID-19, inflation, policy, and FX indicators to explain and forecast hotel demand dynamics across **26 EU countries**.

**Core research question:**  
> Has the European hotel sector returned to its pre-pandemic equilibrium, and which macroeconomic and health factors drive differences in recovery across countries?

---

## 🧾 Data Sources

| Source | Variables | Coverage | Notes |
|-------|-----------|----------|------|
| **Eurostat** | Hotel nights (tour_occ_nim), GDP (quarterly → monthly interpolation), Unemployment (une_rt_m), Turnover index (sts_setu_m), HICP (prc_hicp_midx) | 2015–2025 | Core dataset; GDP monthlyized from quarterly/annual where needed |
| **Our World in Data (OWID)** | COVID-19 new cases (per 100k) | 2020–2024/25 | Filtered to EU; aggregated to **monthly sum per 100k** |
| **Oxford COVID-19 Tracker (OxCGRT)** | Government **Stringency Index** | 2020–2022/24 | **Monthly mean** at country level (EU only) |
| **Exchange Rates (Yahoo Finance)** | EUR/USD, EUR/GBP | 2015–2025 | Monthly close; fallback to alternative sources if needed |

**Final merged dataset (no manipulations beyond joining):**  
`data/processed/hotel_panel.csv`  
- Monthly panel, 26 EU countries, 2015–2025  
- Keys: `region` (ISO-2), `month`  
- **No lags or imputations stored** here; these are created in notebooks

**Analysis-ready (after Notebook 1 Part I):**  
`data/processed/hotel_panel_clean.csv`  
- Interpolated macro series (GDP, turnover), COVID/stringency treated per rules in Notebook 1  
- Same schema plus optional derived fields (`year`, `period` labels)

---

## 🧱 Repository Structure


```
project_root/
│
├── data/
│ ├── raw/
│ │ ├── eurostat_hotels.csv
│ │ ├── covid_cases.csv
│ │ ├── exchange_rates.csv
│ │ └── policy_stringency.csv
│ └── processed/
│ ├── hotel_panel.csv # merged, untouched (no lags/imputation)
│ └── hotel_panel_clean.csv # cleaned/interpolated (Notebook 1)
│
├── src/
│ └── hotel/
│ ├── eurostat_download.py
│ ├── covid_cases_download.py # EU-only, monthly aggregation
│ ├── exchange_rates_download.py # EURUSD=X, EURGBP=X (monthly)
│ ├── policy_stringency_download.py# OxCGRT → monthly mean, EU-only
│ └── merge_datasets.py # merge only (no lags/imputations)
│
├── notebooks/
│ ├── 01-data-exploration.ipynb # EDA, cleaning, imputation, save *_clean.csv
│ ├── 02-forecasting-setup.ipynb # Feature engineering & baselines
│ ├── 03-econometric-modeling.ipynb # Fixed effects, panel regressions
│ ├── 04-ml-models.ipynb # XGBoost, LightGBM, LSTM
│ └── 05-results-visualization.ipynb # Plots & dashboards
│
├── docs/ # exported figures/diagnostics (corr, heatmaps)
├── outputs/
│ ├── figures/
│ └── models/
│
├── README.md
├── pyproject.toml / requirements.txt
└── environment.yml
```


---

## 🔍 Research Design

### Objectives
1. Examine dynamics of hotel demand recovery across Europe (EDA).  
2. Test whether hotel nights returned to pre-COVID equilibrium.  
3. Identify the influence of GDP, unemployment, inflation, COVID, and policy.  
4. **Forecast 12 months ahead** at the country-month level.

### Conceptual Model
\[
\log(\text{NightsSpent}_{it}) = \alpha_i + \delta_t + \beta_1 \log(\text{GDP}_{it}) + \beta_2 \text{Unemployment}_{it} + \beta_3 \text{COVIDCases}_{it} + \beta_4 \text{HICP}_{it} + \varepsilon_{it}
\]

---

## ⚙️ Methods

### Exploratory Data Analysis
- Trends by country and period (Pre-COVID, COVID, Post-COVID)  
- Recovery ratios vs. 2019 baseline  
- Correlation matrices (raw vs within-country)  
- Recovery clusters (k-means on 2019-normalized paths)

### Forecasting & Modeling Framework

| Type | Purpose | Techniques |
|------|--------|------------|
| **Econometric** | Explain recovery | Fixed-effects panel regression; DiD (where relevant) |
| **Forecasting** | **12-month ahead predictions** | **SARIMAX**, **ARIMAX** (with exogenous: GDP, unemployment, HICP, turnover, COVID, stringency, FX) |
| **Machine Learning** | Improve predictive accuracy | **XGBoost**, **LightGBM**, **LSTM** (panel features, rolling CV) |

### Lag Strategy (applied in notebooks, not in raw files)
- GDP & Turnover: 1–3 months  
- COVID: 0–2 months  
- Unemployment: 2–6 months  
- HICP, FX: 1–3 months  
- Seasonality: month dummies / Fourier terms for SARIMAX/ARIMAX

### Evaluation
- Time-based splits / rolling-origin backtesting  
- Metrics: RMSE, MAE, sMAPE; per-country and macro-averaged  
- Benchmark vs. naive (last value) and seasonal-naive

---

## 📈 Preliminary Insights *(to be updated after analysis)*
- Sharp 2020 collapse; heterogeneous recovery by region in 2022–2024.  
- GDP/turnover co-move with hotel nights; COVID incidence and stringency depress demand.  
- ML models expected to outperform linear baselines on multi-feature forecasts.

---

## 🧰 Tools & Libraries
- **Core:** pandas, numpy, requests  
- **Visualization:** matplotlib, seaborn, plotly  
- **Econometrics:** statsmodels, linearmodels  
- **Forecasting:** pmdarima, statsmodels (SARIMAX)  
- **ML:** scikit-learn, xgboost, lightgbm, tensorflow/keras  
- **Geo (optional):** geopandas, folium  
- **Dev:** jupyterlab, black, isort

---

## 🧩 Contributions
- Reproducible EU hotel demand panel (2015–2025) with macro, COVID, HICP, policy, FX  
- Transparent pipeline (download → merge → clean)  
- Comparative evaluation: SARIMAX/ARIMAX vs. ML (XGB/LGBM/LSTM)  
- Open artifacts for policy & academic use

---

## 📚 Citation

> *Author(s)* (2025). **Machine Learning Analysis of Hotel Demand Recovery in Europe After COVID-19.**  
> GitHub Repository: _link_

---

## 🚀 Next Steps
- [x] Add HICP, exchange rates, and policy stringency  
- [x] Finalize EDA & cleaning; save `hotel_panel_clean.csv`  
- [ ] Set up **Notebook 2** (feature engineering + baselines)  
- [ ] Fit SARIMAX/ARIMAX vs XGBoost/LightGBM/LSTM  
- [ ] Model comparison & per-country forecast charts

---

## 📞 Contact

**GitHub:** [@gsanaev](https://github.com/gsanaev)  
**Email:** gsanaev@gmail.com  
**LinkedIn:** [golib-sanaev](https://linkedin.com/in/golib-sanaev)

---

## 🙏 Acknowledgements
- [StackFuel](https://stackfuel.com/) — for supporting applied ML learning  
- [Eurostat](https://ec.europa.eu/eurostat), [Our World in Data](https://github.com/owid/covid-19-data), [Oxford Covid-19 Government Response Tracker (OxCGRT)](https://github.com/OxCGRT/covid-policy-tracker) and [Yahoo Finance](https://finance.yahoo.com) — for open datasets  
- `scikit-learn`, `SHAP`, and `pandas` communities — for transparent ML tools  

---

⭐ **If you find this project insightful, please give it a star!**


