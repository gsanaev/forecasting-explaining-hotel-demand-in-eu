# 🏨 Machine Learning Analysis of Hotel Demand Recovery in Europe After COVID-19

### 📘 Overview
This project analyzes how the European hotel industry has recovered following the COVID-19 pandemic using **machine learning** and **econometric methods**.  
It builds a harmonized Eurostat-based panel dataset (2015–2025) enriched with macroeconomic, COVID-19, and inflation indicators to explain and forecast hotel demand dynamics across 26 EU countries.

**Core research question:**  
> Has the European hotel sector returned to its pre-pandemic equilibrium, and which macroeconomic and health factors drive differences in recovery across countries?

---

## 🧾 Data Sources

| Source | Variables | Coverage | Notes |
|---------|------------|-----------|-------|
| **Eurostat** | Hotel nights, GDP (monthlyized), Unemployment rate, Turnover index, HICP (inflation) | 2015–2025 | Core dataset |
| **ECDC / Our World in Data** | COVID-19 confirmed cases | 2020–2025 | Health shock indicator |
| **Oxford COVID-19 Tracker (OxCGRT)** *(optional)* | Government Stringency Index | 2020–2025 | Lockdown and policy restrictions |
| **European Central Bank (ECB)** *(optional)* | Exchange rates (EUR/USD, EUR/GBP) | 2015–2025 | External competitiveness proxy |

**Final merged dataset:**  
`data/processed/hotel_panel.csv`  
- Monthly panel, 26 EU countries, 2015–2025  
- Includes lagged variables (`gdp_lag1–3`, `covid_cases_lag1–3`, etc.)  
- Derived attributes: `year`, `month`, `period` (*Pre-COVID*, *COVID*, *Post-COVID*)

---

## 🧱 Repository Structure

```
project_root/
│
├── data/
│   ├── raw/                       # Original Eurostat & COVID data
│   ├── processed/                 # Clean merged panel (hotel_panel.csv)
│
├── src/
│   ├── hotel/
│   │   ├── eurostat_download.py   # Downloads Eurostat indicators
│   │   └── merge_datasets.py      # Merges Eurostat, COVID, HICP, etc.
│
├── notebooks/
│   ├── 01-data-exploration.ipynb        # EDA & descriptive analysis
│   ├── 02-feature-engineering.ipynb     # Lags, transformations, normalization
│   ├── 03-econometric-modeling.ipynb    # Fixed-effects & panel regressions
│   ├── 04-machine-learning-models.ipynb # Forecasting (XGBoost, RF, LSTM)
│   ├── 05-results-visualization.ipynb   # Recovery plots & dashboards
│
├── outputs/
│   ├── figures/                # Visualizations & charts
│   ├── models/                 # Trained ML models
│
├── README.md
├── requirements.txt
└── environment.yml
```

---

## 🔍 Research Design

### Objectives
1. Examine the dynamics of hotel demand recovery across Europe (EDA).  
2. Test whether hotel nights have returned to pre-COVID equilibrium levels.  
3. Identify the influence of GDP, unemployment, COVID cases, and inflation.  
4. Forecast hotel demand for 2025–2026 using machine learning.

### Conceptual Model
**Model equation:**

log(NightsSpent_it) = αᵢ + δₜ + β₁·log(GDP_it) + β₂·Unemployment_it + β₃·COVIDCases_it + ε_it


---

## ⚙️ Methods

### Exploratory Data Analysis
- Temporal trends by country and COVID period  
- Recovery ratios vs. 2019 baseline  
- Correlation matrices and elasticity plots  
- Choropleths and small-multiple line charts for EU comparison

### Modeling Framework

| Type | Purpose | Techniques |
|------|----------|-------------|
| **Econometric** | Explain recovery | Fixed-effects panel regression, Difference-in-Differences |
| **Forecasting** | Predict 12-month hotel demand | SARIMAX, ARIMAX |
| **Machine Learning** | Improve predictive accuracy | XGBoost, LightGBM, LSTM |

### Lag Strategy
- GDP & Turnover: 1–3 months delay  
- COVID Cases: 0–2 months delay  
- Unemployment: 2–6 months delay  

---

## 📈 Preliminary Insights *(to be updated after analysis)*
- Hotel activity dropped by ~70% in 2020, partial recovery by 2023.  
- Recovery heterogeneity: Southern Europe rebounded faster post-2022.  
- GDP and turnover strongly correlated with recovery; COVID incidence negatively associated.  
- ML models achieve >85% forecast accuracy *(placeholder)*.

---

## 🧰 Tools & Libraries
- **Core:** `pandas`, `numpy`, `requests`, `tqdm`
- **Visualization:** `matplotlib`, `seaborn`, `plotly`, `geopandas`
- **Econometrics:** `statsmodels`, `linearmodels`
- **Machine Learning:** `scikit-learn`, `xgboost`, `lightgbm`, `tensorflow`
- **Time Series:** `pmdarima`, `prophet`
- **Mapping:** `folium`, `contextily`
- **Dev:** `jupyterlab`, `black`, `isort`

---

## 🧩 Contributions
- Reproducible data pipeline for Eurostat & COVID tourism data  
- Cross-country recovery analysis (2015–2025)  
- Econometric + ML benchmarking for hotel demand forecasting  
- Open-source dataset and code for policy and academic use

---

## 📚 Citation

> *Author(s)* (2025). **Machine Learning Analysis of Hotel Demand Recovery in Europe After COVID-19.**  
> GitHub Repository: [https://github.com/yourusername/machine-learning-hotel-demand-recovery-europe](#)

---

## 🚀 Next Steps
- [ ] Add HICP and optional stringency/exchange-rate indicators  
- [ ] Finalize EDA visualizations  
- [ ] Fit fixed-effects and ML models  
- [ ] Compare recovery speed across countries  
- [ ] Publish summary results and plots  

---

### 📫 Contact
For questions or collaborations, please open an issue or contact **[your.email@domain.eu]**.  
Contributions and replications are warmly welcome.

---
