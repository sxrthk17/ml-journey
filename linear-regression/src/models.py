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

