# 🏨 Forecasting and Explaining Hotel Demand in the European Union (2015–2025) 🌍

> A reproducible **econometric and machine-learning pipeline** for forecasting and interpreting **hotel demand across 26 EU countries (2015–2025)** using macroeconomic and policy indicators.  
> Combines **ARIMAX / SARIMAX** with **XGBoost / LightGBM**, integrating **SHAP explainability**, **panel regression**, and **macroeconomic scenario simulations**.

![Python Version](https://img.shields.io/badge/python-3.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-completed-success)

---

## 📘 View Results Online

Explore the full analytical workflow:

- <a href="https://gsanaev.github.io/forecasting-eu-hotel-demand/01-data-integration-cleaning.html" target="_blank">🧹 Data Integration & Cleaning</a>  
- <a href="https://gsanaev.github.io/forecasting-eu-hotel-demand/02-feature-engineering-exploration.html" target="_blank">🔍 Feature Engineering & Exploration</a>  
- <a href="https://gsanaev.github.io/forecasting-eu-hotel-demand/03-model-training-forecasting.html" target="_blank">⚙️ Model Training & Forecasting</a>  
- <a href="https://gsanaev.github.io/forecasting-eu-hotel-demand/04-model-interpretability.html" target="_blank">📊 Model Interpretability & Economic Drivers</a>  
- <a href="https://gsanaev.github.io/forecasting-eu-hotel-demand/05-scenario-forecasting.html" target="_blank">🌍 Scenario Forecasting & GDP Elasticities</a>  

---

## 📊 Project Overview

**Problem Statement:**  
Tourism demand forecasting is essential for **economic planning, sustainability, and resilience** in Europe.  
While traditional time-series models capture temporal patterns, they often miss **macroeconomic and policy contexts** that drive structural changes.

**Goal:**  
To build a transparent, **hybrid econometric–machine-learning pipeline** that forecasts **monthly hotel nights** across EU countries, identifies their **economic drivers**, and tests **macroeconomic scenarios** for 2025.

**Approach:**  
The workflow integrates:  
- 🧮 **Econometric models:** ARIMAX, SARIMAX  
- 🤖 **Machine learning:** XGBoost, LightGBM  
- 💡 **Explainability:** SHAP values + panel regressions  
- 📈 **Scenario simulations:** GDP, turnover, and policy shocks  

---

## 🎯 Key Insights

- **GDP growth** (current and lagged) remains the **strongest positive determinant** of hotel demand.  
- **Tourism turnover** captures short-run cyclical fluctuations.  
- **Policy stringency** (COVID restrictions) still shows a **negative but declining** effect post-2022.  
- **Unemployment** plays a limited role once GDP and turnover are controlled for.  
- **Scenario simulations (2025)** indicate that small, tourism-intensive economies are **highly elastic**, while large diversified ones are **structurally resilient**.

| Group | Countries | GDP Elasticity | Interpretation |
|--------|------------|----------------|----------------|
| **Highly elastic** | LU, LV, ES, NL | > 1.0 | Tourism activity amplifies macro cycles |
| **Moderately elastic** | SI, CY, HR | 0.5–1.0 | Balanced cyclical response |
| **Stable markets** | DE, FR, BE | < 0.3 | Business travel dominates; less cyclical |

---

## 📁 Repository Structure

```
├── data/                              # All input and processed data
│ ├── raw/                             # 📂 Original data sources
│ │ ├── covid.csv                      # Our World in Data (OWID)
│ │ ├── eurostat.csv                   # Eurostat tourism & macro indicators
│ │ ├── fx_rates.csv                   # Yahoo Finance — exchange rates
│ │ ├── policy_stringency.csv          # Oxford COVID-19 Tracker (OxCGRT)
│ │ └── .gitkeep
│ │
│ ├── interim/                         # 📂 Intermediate cleaned data
│ │ ├── hotel.csv                      # Transitional dataset before modeling
│ │ └── .DS_Store
│ │
│ ├── processed/                       # 📂 Final modeling and forecast datasets
│ │ ├── hotel_clean.csv                # After cleaning and harmonization
│ │ ├── hotel_features.csv             # Feature-engineered dataset
│ │ ├── hotel_predictions.csv          # Combined model forecasts
│ │ ├── hotel_scenario_results.csv     # Scenario simulations (GDP, turnover, policy)
│ │ ├── hotel_scenario_gdp_merged.csv  # Merged baseline + scenario forecasts
│ │ ├── .gitkeep
│ │ └── .DS_Store
│ │
│ └── data_reserve/                    # 📂 Backup snapshots for reproducibility
│ └── hotel_2025-11-01.csv
│
├── src/                               # 📂 Automated data acquisition scripts
│ └── hotel/
│ ├── eurostat_download.py             # Downloads Eurostat data
│ ├── covid_download.py                # Imports OWID COVID data
│ ├── fx_rates_download.py             # Retrieves FX rate data
│ ├── policy_stringency_download.py    # Loads OxCGRT policy data
│ └── hotel_merge.py                   # Merges all raw datasets
│
├── notebooks/                                           # 📓 Analytical notebooks (core workflow)
│ ├── 01_data_exploration_preparation.ipynb              # Data cleaning & integration
│ ├── 02_feature_engineering_forecasting.ipynb           # Feature creation & transformation
│ ├── 03_model_estimation_comparison.ipynb               # ARIMAX, SARIMAX, XGB, LGBM training
│ ├── 04_model_interpretability_economic_drivers.ipynb   # SHAP + panel regressions
│ └── 05_scenario_forecasting_policy_simulations.ipynb   # Scenario forecasting (GDP shocks)
│
├── utils/                             # ⚙️ Custom utility modules
│ ├── metrics.py                       # Evaluation metrics (RMSE, MAE, etc.)
│ ├── modeling.py                      # Preprocessing and ML pipelines
│ ├── plots.py                         # Visualization helpers
│ ├── explainability.py                # SHAP & econometric interpretation
│ └── scenarios.py                     # Scenario simulation and elasticity
│
├── outputs/                           # 📊 Model outputs, reports, visualizations
│ ├── models/                          # Trained models and feature sets
│ │ ├── pipe_xgb.pkl
│ │ ├── pipe_lgbm.pkl
│ │ ├── arimax/                        # Regional ARIMAX models
│ │ ├── sarimax/                       # Regional SARIMAX models
│ │ ├── X_train_shap.parquet
│ │ └── X_train_columns.json
│ │
│ ├── figures/                                  # Visualization outputs (plots & comparisons)
│ │ ├── EU_vs_Top5_Hotel_Nights_COVID.png       # Baseline tourism trend comparison
│ │ ├── correlation_within_vs_raw.png           # Correlation analysis before/after demeaning
│ │ ├── shap_summary_xgb.png                    # SHAP beeswarm summary — XGBoost
│ │ ├── shap_summary_lgbm.png                   # SHAP beeswarm summary — LightGBM
│ │ ├── shap_dependence_xgb_log_gdp_lag1.png    # Feature dependence (GDP lag) — XGB
│ │ ├── gdp_elasticity_by_country.png           # Country-level GDP elasticity
│ │ └── scenario_forecast_comparison_DE.png     # Example scenario forecast — Germany
│ │
│ ├── reports/                         # Tabular outputs and summaries
│ │ └── driver_regression_summary.csv
│ │ └── gdp_elasticity_summary.csv
│ └── .gitkeep
│
├── docs/                              # 🌐 Rendered HTML notebooks for GitHub Pages
│ ├── 01_data_exploration_preparation.html
│ ├── 02_feature_engineering.html
│ ├── 03_model_estimation_comparison.html
│ ├── 04_model_interpretability_economic_drivers.html
│ └── 05_scenario_forecasting_policy_simulations.html
│
├── README.md        # 📄 Main project documentation
└── pyproject.toml   # ⚙️ Environment configuration
```

---

## 🚀 Reproducibility

### Setup
```bash
# Clone the repository
git clone https://github.com/gsanaev/forecasting-explaining-hotel-demand-in-eu.git
cd forecasting-explaining-hotel-demand-in-eu

# Sync environment (installs Python and dependencies)
uv sync
```

### Execution
Ensure raw data is available in `data/raw/`, then run:

```bash
# 1. Retrieve Eurostata data
uv run python -m src.hotel.eurostat_download

# 2. Retrieve Our World in Data (OWID) data
uv run python -m src.hotel.covid_download

# 3. Retrieve Oxford COVID-19 Tracker (OxCGRT) data
uv run python -m src.hotel.policy_stringency_download

# 4. Retrieve Yahoo Finance data
uv run python -m src.hotel.fx_rates_download

# 5. Merge Downloaded data
uv run python -m src.hotel.hotel_merge
```
Finally, execute notebooks in sequence:

```bash
# 1. notebooks/01-data-integration-cleaning.ipynb
# 2. notebooks/02-feature-engineering.ipynb
# 3. notebooks/03-model-training-forecasting.ipynb
# 4. notebooks/04-model-interpretability.ipynb
# 5. notebooks/05-scenario-forecasting.ipynb
```
---

## 📚 Citation
> Sanaev, G. (2025). *Forecasting and Explaining Hotel Demand in the European Union (2015–2025).*  
> GitHub Repository: [github.com/gsanaev/forecasting-explaining-hotel-demand-in-eu](https://github.com/gsanaev/forecasting-explaining-hotel-demand-in-eu)

---

## 📞 Contact

**GitHub:** [@gsanaev](https://github.com/gsanaev)  
**Email:** gsanaev@gmail.com  
**LinkedIn:** [golib-sanaev](https://linkedin.com/in/golib-sanaev)

---

## 🙏 Acknowledgements
- [StackFuel](https://stackfuel.com/) — for supporting applied machine learning research  
- [Elite Hospitality GmbH](https://anorhotels.de/) - for industry collaboration and applied insights
- [Eurostat](https://ec.europa.eu/eurostat) — for open tourism and macroeconomic indicators  
- [Our World in Data (OWID)](https://ourworldindata.org/coronavirus) — for COVID-19 data  
- [Oxford COVID-19 Government Response Tracker (OxCGRT)](https://www.bsg.ox.ac.uk/research/research-projects/covid-19-government-response-tracker) — for policy stringency data  
- [Yahoo Finance](https://finance.yahoo.com/) — for exchange rate data  
- `scikit-learn`, `SHAP`, and `pandas` communities — for open, transparent ML tools  
- **OpenAI Assistant (GPT-5)** — for research collaboration, technical writing, and workflow automation  


⭐ **If you find this project insightful, please give it a star!**
