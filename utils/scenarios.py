"""
===============================================================
Scenario Simulation & Visualization Utilities
===============================================================
Provides reusable functions for scenario-based forecasting
and elasticity analysis of hotel demand models (XGB, LGBM).

Main functions:
- apply_shock(df, shock_type, shock_value)
- simulate_scenario(df, models, scenario_name, shock_type, shock_value)
- plot_gdp_scenarios(df, countries, baseline_col, opt_col, pes_col)
- classify_color(e)

Author: OpenAI Assistant & [Your Name]
Version: 1.0
Last updated: 2025-10-31
===============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


__all__ = [
    "apply_shock",
    "simulate_scenario",
    "plot_gdp_scenarios",
    "classify_color",
]


# ===============================================================
# APPLY MACRO SHOCK
# ===============================================================
def apply_shock(df: pd.DataFrame, shock_type: str, shock_value: float) -> pd.DataFrame:
    """
    Apply a macroeconomic shock (GDP, turnover, policy) to a dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset containing lagged and contemporaneous macro variables.
    shock_type : str
        One of {'none', 'gdp', 'turnover', 'policy'}.
    shock_value : float
        Proportional change to apply (e.g., 0.05 for +5%).

    Returns
    -------
    pd.DataFrame
        Shock-adjusted DataFrame.
    """
    df_scen = df.copy()

    if shock_type == "none":
        return df_scen
    elif shock_type == "gdp":
        mask = df_scen.columns.str.contains("log_gdp", case=False)
    elif shock_type == "turnover":
        mask = df_scen.columns.str.contains("turnover_index", case=False)
    elif shock_type == "policy":
        mask = df_scen.columns.str.contains("stringency", case=False)
    else:
        raise ValueError(f"Unknown shock_type: {shock_type}")

    df_scen.loc[:, mask] = df_scen.loc[:, mask].apply(lambda s: s * (1 + shock_value))
    return df_scen


# ===============================================================
# SCENARIO SIMULATION
# ===============================================================
def simulate_scenario(
    df: pd.DataFrame,
    models: dict,
    scenario_name: str,
    shock_type: str,
    shock_value: float
) -> pd.DataFrame:
    """
    Simulate a scenario with a given macro shock and predictive models.

    Parameters
    ----------
    df : pd.DataFrame
        Future input data (e.g., df_future subset).
    models : dict
        Dictionary of trained model pipelines, e.g. {'xgb': pipe_xgb, 'lgbm': pipe_lgbm}.
    scenario_name : str
        Name of the scenario (e.g., 'optimistic_gdp').
    shock_type : str
        Type of macro variable shocked ('gdp', 'turnover', 'policy', or 'none').
    shock_value : float
        Magnitude of the shock (e.g., +0.05 for +5%).

    Returns
    -------
    pd.DataFrame
        DataFrame with predicted columns appended per model, e.g. 'yhat_xgb_optimistic_gdp'.
    """
    print(f"⚙️ Running scenario: {scenario_name} ({shock_type}, {shock_value:+.2%})")

    df_scen = apply_shock(df, shock_type, shock_value)
    df_out = df_scen.copy()

    for model_name, pipeline in models.items():
        try:
            if hasattr(pipeline, "named_steps") and "pre" in pipeline.named_steps:
                pre = pipeline.named_steps["pre"]
                model = pipeline.named_steps["model"]
                X = pre.transform(df_scen)
                preds = model.predict(X)
            else:
                X = df_scen.select_dtypes(include=[np.number])
                preds = pipeline.predict(X)

            df_out[f"yhat_{model_name}_{scenario_name}"] = preds
            print(f"✅ Scenario simulated for {model_name}")
        except Exception as e:
            print(f"⚠️ {model_name} failed during {scenario_name}: {e}")

    if "month" in df_out.columns:
        df_out["month"] = pd.to_datetime(df_out["month"], errors="coerce")

    return df_out


# ===============================================================
# PLOT GDP SCENARIOS (LOG SCALE)
# ===============================================================
def plot_gdp_scenarios(df, countries, baseline_col, opt_col, pes_col, save_dir=None):
    """
    Visualize baseline vs optimistic/pessimistic GDP scenarios (log scale),
    and optionally save each country's figure to disk.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing baseline and scenario predictions.
    countries : list of str
        List of region codes (e.g. ['DE', 'FR', 'IT']).
    baseline_col, opt_col, pes_col : str
        Column names for baseline, optimistic, and pessimistic predictions.
    save_dir : str or Path, optional
        Directory to save figures. If None, figures are only shown.
    """
    if save_dir is not None:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

    for country in countries:
        sub = df[df["region"] == country].sort_values("month")
        if sub.empty:
            print(f"⚠️ No data for {country}")
            continue

        fig, axes = plt.subplots(1, 2, figsize=(10, 3), sharey=True)

        # --- Left: Baseline vs Optimistic
        axes[0].plot(sub["month"], sub[baseline_col], label="Baseline", lw=2)
        axes[0].plot(sub["month"], sub[opt_col], label="Optimistic GDP",
                     lw=2, ls="--", color="green")
        axes[0].set_title(f"{country} — Optimistic Scenario")
        axes[0].set_xlabel("Month")
        axes[0].set_ylabel("Predicted hotel nights (log scale)")
        axes[0].legend(frameon=False)
        axes[0].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

        # --- Right: Baseline vs Pessimistic
        axes[1].plot(sub["month"], sub[baseline_col], label="Baseline", lw=2)
        axes[1].plot(sub["month"], sub[pes_col], label="Pessimistic GDP",
                     lw=2, ls="--", color="red")
        axes[1].set_title(f"{country} — Pessimistic Scenario")
        axes[1].set_xlabel("Month")
        axes[1].legend(frameon=False)
        axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

        plt.suptitle(f"GDP Scenario Comparison — {country}", fontsize=12)
        plt.tight_layout()

        # --- Save each figure if requested
        if save_dir is not None:
            fig_path = save_dir / f"scenario_forecast_comparison_{country}.png"
            plt.savefig(fig_path, dpi=300, bbox_inches="tight")
            print(f"💾 Saved figure for {country} → {fig_path}")

        plt.show()


# ===============================================================
# ELASTICITY COLOR CLASSIFIER
# ===============================================================
def classify_color(e: float) -> str:
    """
    Classify elasticity into color categories for visualization.

    Parameters
    ----------
    e : float
        Elasticity value (Δ% Demand / Δ% GDP).

    Returns
    -------
    str
        Color code.
    """
    if e >= 1:
        return "mediumseagreen"   # highly elastic
    elif e >= 0.5:
        return "gold"             # moderately elastic
    else:
        return "lightgray"        # low elasticity
    

# ===============================================================
# SCENARIO IMPACT (% CHANGE) CALCULATION
# ===============================================================
def calculate_impact(df_plot):
    """
    Compute percentage change vs baseline for optimistic and pessimistic GDP scenarios.

    Parameters
    ----------
    df_plot : pd.DataFrame
        Must contain columns:
        ['region', 'month', 'yhat_xgb',
         'yhat_xgb_optimistic_gdp', 'yhat_xgb_pessimistic_gdp']

    Returns
    -------
    pd.DataFrame
        impact_summary : mean % deviation by region (for optimistic and pessimistic scenarios)
    """
    df_impact = df_plot.copy()[[
        "region", "month",
        "yhat_xgb", "yhat_xgb_optimistic_gdp", "yhat_xgb_pessimistic_gdp"
    ]]

    for col in ["yhat_xgb_optimistic_gdp", "yhat_xgb_pessimistic_gdp"]:
        scen = col.replace("yhat_xgb_", "")
        df_impact[f"{scen}_pct_diff"] = (
            (df_impact[col] - df_impact["yhat_xgb"]) / df_impact["yhat_xgb"]
        ) * 100

    impact_summary = (
        df_impact.groupby("region")[["optimistic_gdp_pct_diff", "pessimistic_gdp_pct_diff"]]
        .mean()
        .sort_values("optimistic_gdp_pct_diff", ascending=False)
    )

    return impact_summary


# ===============================================================
# GDP ELASTICITY CALCULATION
# ===============================================================
def calculate_elasticity(df_impact, shock_size=0.10):
    """
    Compute GDP elasticity of demand for each region.

    Parameters
    ----------
    df_impact : pd.DataFrame
        DataFrame with columns:
        ['region', 'optimistic_gdp_pct_diff', 'pessimistic_gdp_pct_diff']
    shock_size : float, default=0.10
        Total GDP change between optimistic and pessimistic scenarios.
        (e.g., ±5% => total 10% = 0.10)

    Returns
    -------
    pd.DataFrame
        DataFrame with region, elasticity, and color classification.
    """
    df_elast = df_impact.copy()

    # Ensure region is a column
    if "region" not in df_elast.columns:
        df_elast = df_elast.reset_index()

    # Compute elasticity: ΔDemand% / ΔGDP%
    df_elast["gdp_elasticity"] = (
        (df_elast["optimistic_gdp_pct_diff"] - df_elast["pessimistic_gdp_pct_diff"])
        / (shock_size * 100)
    )

    # Classify visually
    df_elast["color"] = df_elast["gdp_elasticity"].apply(classify_color)

    return df_elast

