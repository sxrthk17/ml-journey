import numpy as np

class SimpleLinearRegression:
    def __init__(self):
        self.beta_0 = None
        self.beta_1 = None

    def fit(self, X:np.ndarray, y:np.ndarray):

        if len(X) != len(y):
            raise ValueError("X and y must have same number of samples")

        x_centered = X - np.mean(X)
        y_centered = y - np.mean(y)
        covariance = np.mean((x_centered * y_centered))
        variance = np.mean((x_centered)**2)

        if variance == 0:
            raise ZeroDivisionError("variance value found to be 0")
        
        self.beta_1 = covariance / variance
        self.beta_0 = np.mean(y) - (self.beta_1 * np.mean(X))
        return self

    def predict(self, X:np.array):
        if self.beta_0 is None or self.beta_1 is None:
            raise ValueError("Model is not fitted! Call .fit() first")


        return self.beta_0 + (self.beta_1 * X)

    def r2_score(self, X:np.ndarray, y:np.ndarray):
        y_pred = self.predict(X)
        ss_residual = np.sum((y - y_pred) ** 2)
        ss_total = np.sum((y - np.mean(y)) ** 2)
        if ss_total == 0:
            return 0.0
        return 1 - (ss_residual / ss_total)


class MultipleLinearRegression:
    def __init__(self):
        self.beta_hat = None
        self.intercept_ = None
        self.coef_ = None
        
    def _add_intercept(self, X):
        X = np.asarray(X, dtype=float)

        return np.c_[np.ones(X.shape[0]), X]

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)

    
        X_design = self._add_intercept(X)

        XTX = X_design.T @ X_design

        XTy = X_design.T @ y

        self.beta_hat = np.linalg.solve(XTX, XTy)
        self.intercept_ = self.beta_hat[0]
        self.coef_ = self.beta_hat[1:]

        return self

    def predict(self, X):
        if self.beta_hat is None:
            raise ValueError("Model is not fitted yet! Call fit() first")
        X = np.asarray(X, dtype=float)
        X_test_design = self._add_intercept(X)
        
        return X_test_design @ self.beta_hat

    def residual(self, X, y):
        y = np.asarray(y, dtype=float)
        y_pred = self.predict(X)
        resid = y - y_pred
        return resid

    def r2_score(self,X ,y):
        y = np.asarray(y, dtype=float)

        y_pred = self.predict(X)

        ss_residual = np.sum((y - y_pred) ** 2)

        ss_total = np.sum((y - np.mean(y)) ** 2)

        if ss_total == 0.0:
            return 0

        return 1 - (ss_residual / ss_total)
