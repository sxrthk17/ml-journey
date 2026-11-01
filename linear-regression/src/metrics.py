import numpy as np

def _validate_y(y_true):
    y_true = np.asarray(y_true)
    if y_true.size == 0:
        raise ValueError("Input array cannot be empty.")
    if not np.isfinite(y_true).all():
        raise ValueError("Inputs contain NaN or infinite values.")
    return y_true


def _validate_predictions(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    if y_true.size == 0 or y_pred.size == 0:
        raise ValueError("Input arrays cannot be empty.")

    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"Shape mismatch: y_true shape {y_true.shape} must match y_pred shape"
            f" {y_pred.shape}"
        )

    if not np.isfinite(y_true).all() or not np.isfinite(y_pred).all():
        raise ValueError("Inputs contain NaN or infinite values.")
    return y_true, y_pred

def r2_score(y_true, y_pred):
    y_true, y_pred = _validate_predictions(y_true, y_pred)

    sse = np.sum((y_true - y_pred) ** 2)
    sst = np.sum((y_true - np.mean(y_true)) ** 2)

    if np.isclose(sst, 0.0, atol=1e-8):
    # Scikit-learn convention typically returns 0.0 or 1.0 depending on predictions,
    # but returning 0.0 or a safe default is standard.
        return 0.0

    if sst == 0.0:
        return 0
    return 1 - (sse/sst)

def adjusted_r2score(X, y_true, y_pred):
    y_true, y_pred = _validate_predictions(y_true, y_pred)
    
    X = np.asarray(X)
    if X.size == 0:
        raise ValueError("Feature matrix X cannot be empty.")
    if X.shape[0] != y_true.shape[0]:
        raise ValueError(
        f"Sample size mismatch: X has {X.shape[0]} rows, but y_true has"
        f" {y_true.shape[0]} elements.")
    
    sse = np.sum((y_true - y_pred) ** 2)
    sst = np.sum((y_true - np.mean(y_true)) ** 2)

    n = y_true.shape[0]

    p = X.shape[1] if len(X.shape) > 1 else 1

    if np.isclose(sst, 0.0, atol=1e-8):
    # Scikit-learn convention typically returns 0.0 or 1.0 depending on predictions,
    # but returning 0.0 or a safe default is standard.
        return 0.0

    if n - p - 1 <=0:
        return 0.0

    adjusted_r2 = 1 - (sse/(n-p-1)) / (sst/ (n - 1))

    return adjusted_r2

def mse(y_true, y_pred):
    y_true, y_pred = _validate_predictions(y_true, y_pred)
    residual = y_true - y_pred
    return np.mean((residual)**2)

def root_mse(y_true, y_pred):
    y_true, y_pred = _validate_predictions(y_true, y_pred)
    residual = y_true - y_pred
    mse_val = np.mean((residual)**2)
    return np.sqrt(mse_val)

def mean_absolute_error(y_true, y_pred):
    y_true, y_pred = _validate_predictions(y_true, y_pred)
    abs_error = np.abs(y_true - y_pred)
    return np.mean(abs_error)

def total_sum_of_squares(y_true):
    y_true = _validate_y(y_true)
    return np.sum((y_true - np.mean(y_true)) ** 2)

def model_sum_of_squares(y_true, y_pred):
    y_true, y_pred = _validate_predictions(y_true, y_pred)
    return np.sum((y_pred - np.mean(y_true)) ** 2)

def sum_of_squared_error(y_true, y_pred):
    y_true, y_pred = _validate_predictions(y_true, y_pred)
    return np.sum((y_true - y_pred) ** 2)

def calculate_metrics(y_true, y_pred):
    pass