# utils/explainability.py
import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# ===============================================================
# SHAP UTILITIES
# ===============================================================

def compute_shap_values(model, X, background_size=500):
    """
    Compute SHAP values for tree-based models (XGBoost, LightGBM, etc.).
    Includes auto-detection for pipelines and safe fallback mode.
    """
    # --- Handle sklearn pipelines ---
    if hasattr(model, "named_steps") and "model" in model.named_steps:
        model = model.named_steps["model"]

    # --- Sample background for efficiency ---
    bg_size = min(background_size, len(X))
    X_bg = X.sample(bg_size, random_state=42)

    # --- Try fast TreeExplainer ---
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X_bg)
        print(f"✅ TreeExplainer succeeded for {model.__class__.__name__}.")
        return explainer, shap_values

    # --- Fallback (e.g. XGBoost error: not callable) ---
    except Exception as e:
        print(f"⚠️ TreeExplainer failed: {e}")
        print("→ Using fallback (PermutationExplainer, safe mode).")
        explainer = shap.Explainer(model.predict, X_bg)
        shap_values = explainer(X_bg)
        print("✅ SHAP values computed successfully (safe mode).")
        return explainer, shap_values

def summarize_shap(shap_values, X=None, model_name="Model"):
    """
    Generate SHAP beeswarm and bar plots for a given model.
    Automatically uses shap_values.data if X is None.
    """
    if X is None:
        X = getattr(shap_values, "data", None)
        if X is None:
            raise ValueError("No feature data provided and shap_values.data is missing.")

    print(f"🔹 Plotting {model_name} SHAP summaries...")

    plt.figure()
    shap.summary_plot(shap_values, X, max_display=15, show=False)
    plt.title(f"{model_name} — SHAP Beeswarm Summary")
    plt.tight_layout()
    plt.show()

    plt.figure()
    shap.summary_plot(shap_values, X, plot_type="bar", max_display=15, show=False)
    plt.title(f"{model_name} — Global Feature Importance")
    plt.tight_layout()
    plt.show()

def dependence_plot(shap_values, X, feature_name, model_name="Model"):
    """
    Generate a SHAP dependence plot for a specific feature.
    Works for both TreeExplainer and PermutationExplainer outputs.
    """
    # --- Use fallback to shap_values.data if X not provided ---
    if X is None:
        X = getattr(shap_values, "data", None)
        if X is None:
            raise ValueError("No feature data provided and shap_values.data is missing.")

    # --- Extract SHAP matrix robustly ---
    if hasattr(shap_values, "values"):
        shap_matrix = shap_values.values
    elif isinstance(shap_values, np.ndarray):
        shap_matrix = shap_values
    else:
        shap_matrix = np.array(shap_values)

    # --- Safety alignment ---
    n = min(len(X), shap_matrix.shape[0])
    shap_matrix = shap_matrix[:n, :]
    X = X.iloc[:n, :]

    print(f"📈 Plotting SHAP dependence for '{feature_name}' — {model_name}")

    shap.dependence_plot(
        feature_name,
        shap_matrix,
        X,
        feature_names=X.columns,
        show=False
    )
    plt.title(f"{model_name} — SHAP Dependence: {feature_name}")
    plt.tight_layout()
    plt.show()


# ===============================================================
# ECONOMETRIC / REGRESSION INTERPRETATION
# ===============================================================

def run_panel_regression(df: pd.DataFrame, y: str, X_vars: list, fe: str | None = None):
    """
    Run a simple OLS or fixed-effects regression on SHAP or macro drivers.
    Example:
        run_panel_regression(df, 'yhat_lgbm', ['log_gdp', 'turnover_index'], fe='region')
    """
    data = df.dropna(subset=[y] + X_vars).copy()
    y_data = data[y]
    X_data = sm.add_constant(data[X_vars])

    if fe and fe in data.columns:
        dummies = pd.get_dummies(data[fe], drop_first=True, prefix=fe)
        X_data = pd.concat([pd.DataFrame(X_data), pd.DataFrame(dummies)], axis=1)

    model = sm.OLS(y_data, X_data).fit()
    return model
