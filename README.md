# 🏨 Machine Learning and Econometric Analysis of Hotel Demand Recovery in Europe (2015–2026)

### 📘 Overview
This project analyzes how the **European hotel industry** has recovered following the COVID-19 pandemic using **econometric** and **machine-learning** methods.  
It constructs a harmonized **monthly panel (2015–2026)** for 26 EU countries using data from Eurostat, Our World in Data, Oxford COVID-19 Tracker, and Yahoo Finance to forecast and explain hotel demand dynamics.

**Core research question:**  
> Has the European hotel sector returned to its pre-pandemic equilibrium, and which macroeconomic and health factors drive differences in recovery across countries?

---

## 🧾 Data Sources

| Source | Variables | Coverage | Notes |
|-------|-----------|----------|------|
| **Eurostat** | Hotel nights, GDP (monthlyized), Unemployment, Turnover index, HICP | 2015–2025 | Core dataset |
| **Our World in Data (OWID)** | COVID-19 new cases per 100k | 2020–2025 | Aggregated to monthly sums |
| **Oxford COVID-19 Tracker (OxCGRT)** | Government **Stringency Index** | 2020–2023 | Monthly mean per country |
| **Yahoo Finance** | EUR/USD, EUR/GBP exchange rates | 2015–2025 | Monthly close prices |

**Main processed datasets**
- `hotel_panel_clean.csv` — cleaned harmonized monthly panel  
- `hotel_panel_features.csv` — feature-engineered dataset (lags, MoM, time vars)  
- `model_predictions.csv` — model outputs and forecasts  

---

## 🧱 Repository Structure


```
project_root/
│
├── data/
│ ├── raw/ # Original Eurostat, OWID, OxCGRT, FX data
│ └── processed/
│ ├── hotel_panel.csv
│ ├── hotel_panel_clean.csv
│ ├── hotel_panel_features.csv
│ └── model_predictions.csv
│
├── src/hotel/ # Python scripts for data acquisition and merging
│
├── notebooks/
│ ├── 01-data-exploration.ipynb
│ ├── 02-feature-engineering-and-forecasting.ipynb
│ ├── 03-advanced-forecasting.ipynb
│ ├── 04-econometric-and-interpretability.ipynb
│ └── 05-results-visualization.ipynb
│
├── outputs/
│ ├── figures/ # Plots, dashboards, recovery maps
│ ├── models/ # Trained models or serialized results
│ └── tables/ # Evaluation and regression summaries
│
├── docs/ # Exported visualizations / reports
│
├── pyproject.toml / requirements.txt
├── environment.yml
└── README.md
```

---


---

## 🧭 Notebook Overview

| # | Notebook | Title | Purpose |
|---|-----------|--------|----------|
| **01** | `01-data-exploration.ipynb` | **Data Exploration and Cleaning** | Merge raw Eurostat, OWID, OxCGRT, FX data; interpolate missing values; produce `hotel_panel_clean.csv`. |
| **02** | `02-feature-engineering-and-forecasting.ipynb` | **Feature Engineering & Baseline Forecasting** | Create lagged/MoM/time features; train Naïve, ARIMAX, XGBoost baselines; export `hotel_panel_features.csv`. |
| **03** | `03-advanced-forecasting.ipynb` | **Advanced Forecasting Models** | Extend forecasting with SARIMAX, XGBoost, LightGBM, and LSTM; compare RMSE/MAE across EU markets. |
| **04** | `04-econometric-and-interpretability.ipynb` | **Econometric & Interpretability Analysis** | Estimate fixed-effects and DiD regressions; apply SHAP analysis to explain ML model behavior. |
| **05** | `05-results-visualization.ipynb` | **Results Visualization & Policy Insights** | Create comparative plots, recovery dashboards, and summarize main findings. |

---

### 🔄 Project Workflow Summary

1. **Data Collection & Cleaning (Notebook 1):**  
   Raw hotel, macroeconomic, and policy data merged and harmonized into a monthly EU panel.  
2. **Feature Engineering & Baseline Forecasting (Notebook 2):**  
   Create lag/MoM/time features and build baseline Naïve, ARIMAX, XGBoost forecasts.  
3. **Advanced Forecasting (Notebook 3):**  
   Develop and compare SARIMAX, XGBoost, LightGBM, and LSTM models for 2025–2026.  
4. **Econometric & Interpretability Analysis (Notebook 4):**  
   Quantify macroeconomic and policy impacts using fixed-effects regressions and SHAP.  
5. **Visualization & Policy Insights (Notebook 5):**  
   Aggregate results and visualize recovery patterns across EU countries.

---

### 🗺️ Data Flow Overview

RAW DATA SOURCES
↓
01-data-exploration.ipynb
→ hotel_panel_clean.csv
↓
02-feature-engineering-and-forecasting.ipynb
→ hotel_panel_features.csv
↓
03-advanced-forecasting.ipynb
→ model_predictions.csv
↓
04-econometric-and-interpretability.ipynb
→ econometric_results.csv / SHAP tables
↓
05-results-visualization.ipynb
→ dashboards / policy charts


> This modular design ensures full reproducibility — from raw data ingestion to interpretable forecasting and policy-level insights.

---

## ⚙️ Methods & Tools

| Category | Libraries / Techniques |
|-----------|------------------------|
| **Core** | pandas, numpy, requests |
| **Econometrics** | statsmodels, linearmodels |
| **Forecasting** | pmdarima, SARIMAX, XGBoost, LightGBM, TensorFlow/Keras (LSTM) |
| **Interpretability** | SHAP, feature importance |
| **Visualization** | matplotlib, seaborn, plotly |
| **Geo (optional)** | geopandas, folium |
| **Development** | jupyterlab, black, isort |

---

## 📈 Key Insights (preliminary)

- Sharp demand collapse in 2020 followed by gradual, heterogeneous recovery (2022–2025).  
- GDP and turnover show strong positive correlations with hotel nights, while COVID cases and policy stringency exert negative effects.  
- **XGBoost and LightGBM** outperform linear baselines on multi-feature forecasts.  
- **Econometric results** confirm significant macroelasticities and cross-country heterogeneity in recovery speed.

---

## 🧩 Contributions
- Reproducible EU hotel demand panel (2015–2026) enriched with macroeconomic and COVID variables  
- Transparent pipeline: from data acquisition to model comparison  
- Integrated econometric + ML framework for forecasting and interpretation  
- Open datasets and code for academic and policy research

---

## 📚 Citation
> Sanaev, G. (2025). *Machine Learning and Econometric Analysis of Hotel Demand Recovery in Europe.*  
> GitHub Repository: [github.com/gsanaev/hotel-demand-recovery](https://github.com/gsanaev/hotel-demand-recovery)

---

## 📞 Contact
**GitHub:** [@gsanaev](https://github.com/gsanaev)  
**Email:** gsanaev@gmail.com  
**LinkedIn:** [Golib Sanaev](https://linkedin.com/in/golib-sanaev)

---

⭐ **If you find this project insightful, please give it a star!**
