from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import joblib
from typing import List

# ---------- Preprocessor ----------
def build_preprocessor(cat_cols: List[str], num_cols: List[str]) -> ColumnTransformer:
    cat = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    num = MinMaxScaler()
    return ColumnTransformer(
        transformers=[
            ("cat", cat, cat_cols),
            ("num", num, num_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

# ---------- Models ----------
def build_xgb() -> XGBRegressor:
    return XGBRegressor(
        n_estimators=800,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        tree_method="hist",
        n_jobs=-1,
    )

def build_lgbm() -> LGBMRegressor:
    return LGBMRegressor(
        n_estimators=800,
        learning_rate=0.03,
        max_depth=-1,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        n_jobs=-1,
    )

# ---------- Training helpers ----------
def train_global_pipeline(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    cat_cols: List[str],
    num_cols: List[str],
    model_type: str = "xgb",
):
    pre = build_preprocessor(cat_cols, num_cols)
    model = build_xgb() if model_type == "xgb" else build_lgbm()
    pipe = Pipeline([("pre", pre), ("model", model)])
    pipe.fit(X_train[cat_cols + num_cols], y_train)
    return pipe

def predict_with_pipeline(pipe, X: pd.DataFrame) -> np.ndarray:
    return pipe.predict(X)

def train_region_lgbm_and_dump(
    train: pd.DataFrame,
    valid: pd.DataFrame,
    cat_cols: List[str],
    num_cols: List[str],
    target: str,
    models_dir: Path,
) -> pd.DataFrame:
    models_dir.mkdir(parents=True, exist_ok=True)
    preds = []
    for region, tr in train.groupby("region"):
        vl = valid[valid["region"] == region]
        if len(tr) < 24 or len(vl) == 0:
            continue
        pipe = Pipeline([("pre", build_preprocessor(cat_cols, num_cols)),
                         ("model", build_lgbm())])
        pipe.fit(tr[cat_cols + num_cols], tr[target].values)
        vl = vl.copy()
        vl["yhat_lgbm"] = pipe.predict(vl[cat_cols + num_cols])
        preds.append(vl[["region", "month", "yhat_lgbm"]])
        joblib.dump(pipe, models_dir / f"lgbm_{region}.pkl")
    return pd.concat(preds, ignore_index=True) if preds else pd.DataFrame(columns=["region","month","yhat_lgbm"])
