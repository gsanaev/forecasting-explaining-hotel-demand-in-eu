from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def rmse(y, yhat):
    """Root Mean Squared Error"""
    return float(np.sqrt(mean_squared_error(y, yhat)))

def mae(y, yhat):
    """Mean Absolute Error"""
    return float(mean_absolute_error(y, yhat))

def mape(y, yhat, eps=1e-9):
    """Mean Absolute Percentage Error (safe for near-zero values)"""
    y = np.asarray(y)
    yhat = np.asarray(yhat)
    return float(np.mean(np.abs((y - yhat) / (np.abs(y) + eps))) * 100)