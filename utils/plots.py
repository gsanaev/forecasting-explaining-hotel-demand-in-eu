# utils/plots.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# ===============================================================
# Generic side-by-side comparison plotting
# ===============================================================

def plot_side_by_side(subset: pd.DataFrame, col_actual: str, col_model: str, ax, title: str):
    """Helper to plot Actual vs Model on one axis."""
    ax.plot(
        subset["month"], subset[col_actual],
        label="Actual", marker="o", markersize=3, lw=1.5
    )
    if col_model in subset.columns:
        ax.plot(
            subset["month"], subset[col_model],
            label=f"{title.split(' ')[0]} (predicted)", linestyle="--", lw=1.2
        )
    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, linestyle="--")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# ===============================================================
# Econometric model comparison (ARIMAX vs SARIMAX)
# ===============================================================

def compare_econometric_models(df: pd.DataFrame, top_regions: list):
    """Plots ARIMAX vs SARIMAX for top EU countries."""
    plt.rcdefaults()
    for country in top_regions:
        subset = df.query("region == @country").sort_values("month")
        fig, axes = plt.subplots(1, 2, figsize=(14, 4), sharey=True)
        
        plot_side_by_side(subset, "log_nights_spent", "yhat_arimax", axes[0], f"ARIMAX vs Actual – {country}")
        axes[0].set_ylabel("Log of hotel nights")

        plot_side_by_side(subset, "log_nights_spent", "yhat_sarimax", axes[1], f"SARIMAX vs Actual – {country}")
        
        plt.tight_layout()
        plt.show()

# ===============================================================
# Machine Learning model comparison (XGBoost vs LightGBM)
# ===============================================================

def compare_ml_models(df: pd.DataFrame, top_regions: list):
    """Plots XGBoost vs LightGBM for top EU countries."""
    plt.rcdefaults()
    for c in top_regions:
        subset = df.query("region == @c").sort_values("month")
        fig, axes = plt.subplots(1, 2, figsize=(14, 4), sharey=True)

        plot_side_by_side(subset, "log_nights_spent", "yhat_xgb", axes[0], f"XGBoost vs Actual – {c}")
        axes[0].set_ylabel("Log of hotel nights")

        plot_side_by_side(subset, "log_nights_spent", "yhat_lgbm", axes[1], f"LightGBM vs Actual – {c}")
        
        plt.tight_layout()
        plt.show()
