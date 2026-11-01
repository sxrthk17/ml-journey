import numpy as np

#====================================================================================
# SIMPLE LINEAR REGRESSION
#====================================================================================


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

    def residual(self, X, y):
        y = np.asarray(y)
        y_pred = self.predict(X)
        resid = y - y_pred
        return resid

    def r2_score(self, X:np.ndarray, y:np.ndarray):
        y_pred = self.predict(X)
        ss_residual = np.sum((y - y_pred) ** 2)
        ss_total = np.sum((y - np.mean(y)) ** 2)
        if ss_total == 0:
            return 0.0
        return 1 - (ss_residual / ss_total)


#====================================================================================
# MULTIPLE LINEAR REGRESSION
#====================================================================================
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


#====================================================================================
# GRADIENT DESCENT
#====================================================================================

class GDLinearRegression:
    def __init__(self):
        self.beta_hat = None
        self.intercept_ = None
        self.coef_ = None
        self.loss_history_ = None
        self.lr_ = None
        self.lr_limit_ = None
        self.n_iter_ = None


    def _add_intercept(self, X):
        X = np.asarray(X, dtype=float)

        return np.c_[np.ones(X.shape[0]), X]

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)

        X_design = self._add_intercept(X)

        XTX = X_design.T @ X_design

        XTy = X_design.T @ y

        cond_number = np.linalg.cond(XTX)
        print(f"Condition Number: {cond_number}")

        self.beta_hat = np.linalg.solve(XTX, XTy)
        self.intercept_ = self.beta_hat[0]
        self.coef_ = self.beta_hat[1:]

        return self

    def fit_gd(self, X, y, lr_=None, epochs=1000, tolerance=1e-3):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        X = self._add_intercept(X)
        XTX = X.T @ X
        n = X.shape[0]

        H = (2/n) * XTX
        eigen_values = np.linalg.eigvalsh(H)


        max_ev = np.max(eigen_values)
        cond_number = max_ev / np.min(eigen_values)
        print(f"Condition Number: {cond_number}")
        min_ev = np.min(eigen_values)
        print("Min Eigen Value: ", min_ev)

        self.lr_limit_ = 2 / max_ev
        self.lr_ = lr_ if lr_ is not None else 1 / max_ev
        print(f"Learning Rate: {self.lr_} Limit: {self.lr_limit_}, Max Eigen value: {max_ev}")

        if self.lr_ >= self.lr_limit_:
            print("Warning: lr_ is at or above the stability limit, expect divergence")

        self.beta_hat = np.zeros(X.shape[1]) # jitne columns h, utne B aur ek intercept ke liye pehla wala !!
        
        self.loss_history_ = []
        self.n_iter_ = epochs
        for epoch in range(epochs):
            y_pred = X @ self.beta_hat
            gradient = -(2/n) * X.T @(y - y_pred)
            self.beta_hat = self.beta_hat - self.lr_ * gradient
            loss = np.mean((y - y_pred) ** 2)
            self.loss_history_.append(loss)
            self.n_iter_ = epoch + 1


            if not np.isfinite(loss):
                print("Diverged at epoch:", epoch)
                break

            if epoch > 0 and abs(self.loss_history_[-2] - self.loss_history_[-1]) < tolerance:
                print("Converged at epoch: ", epoch)
                break

        self.intercept_ = self.beta_hat[0] ## B0
        self.coef_ = self.beta_hat[1:] ## B1 to Bn
        return self

    def predict(self, X):
        if self.beta_hat is None:
            raise ValueError("Model is not fitted yet! Please Call .fit() first")
        X = np.asarray(X, dtype=float)
        X_test_design = self._add_intercept(X)
        return X_test_design @ self.beta_hat

    def residual(self, X, y):
        y = np.asarray(y, dtype=float)
        y_pred = self.predict(X)

        residual = y - y_pred
        return residual

    def r2_score(self, X, y):
        y = np.asarray(y, dtype=float)

        y_pred = self.predict(X)

        ss_residual = np.sum((y - y_pred) ** 2)
        ss_total = np.sum((y- np.mean(y)) ** 2)

        if ss_total == 0.0:
            return 0

        return 1 - (ss_residual/ss_total)

#====================================================================================
# STOCHIASTIC GRADIENT DESCENT OR MINI BATCH GRADIENT DESCENT
#====================================================================================

class SGDLinearRegression():
    def __init__(self):
        self.beta_hat = None
        self.coef_ = None
        self.intercept_ = None
        self.lr_ = None
        self.lr_limit_ = None
        self.loss_history_ = None
        self.n_iter_ = None
        self.lr0_ = None
        self.lr_history_ = None
        self.stop_reason_ = 'max_epochs'
        self.final_loss_ = None

    def _add_intercept(self, X):
        X = np.asarray(X, float)
        return np.c_[np.ones(X.shape[0]), X]

    def _current_lr(self, epoch, lr0, decay_type=None, decay_rate=0.0):
        if decay_type is None:
            return lr0
        
        if decay_type == "time":
                return lr0 / (1 + decay_rate * epoch)

        elif decay_type == "exponential":
                return lr0 * np.exp(-decay_rate * epoch)

        else:
            raise ValueError(f"Decay type: {decay_type} not supported:\nSupported types : ['time', 'exponential']")

    def fit_sgd(self, X, y, batch_size=None,  epochs=1000, lr=None, tolerance=1e-08, decay_rate=0.0, decay_type=None, shuffle=True, seed=42):
        X = np.asarray(X, float)
        y = np.asarray(y, float).ravel()

        X = self._add_intercept(X)
        self.beta_hat = np.zeros(X.shape[1])

        XTX = X.T @ X
        n = X.shape[0]
        H = (2/n) * XTX

        eigen_values = np.linalg.eigvalsh(H)
        max_ev = np.max(eigen_values)

        self.lr_ = lr if lr is not None else 1/max_ev
        self.lr_limit_ = 2/max_ev
        self.lr0_ = self.lr_
        self.stop_reason_ = "max_epochs"

        if self.lr_ >= self.lr_limit_:
            print("Warning! lr_ is at or above the stability limit, expect divergence.")

        self.loss_history_ = []
        self.n_iter_ = epochs
        self.lr_history_ = []
        

        if batch_size is None: #if batch size isnot given, take the whole array of X
            batch_size = X.shape[0]
        else:
            batch_size = min(batch_size, n)
        rng = np.random.default_rng(seed) #seed to keep a fixed start okay !!

        for epoch in range(epochs):

            self.lr_ = self._current_lr(epoch, self.lr0_, decay_rate=decay_rate, decay_type=decay_type)
            
            indices = np.arange(len(X))
            if shuffle:
                rng.shuffle(indices)

            y_pred = X @ self.beta_hat #fit the whole complete X with the current beta get the loss and chec is loss is finite or not ! 
            loss = np.mean((y - y_pred)**2) #recording full dataset loss each epoch, before updates. 

            if not np.isfinite(loss):
                self.stop_reason_ = 'divergence'
                break

            self.loss_history_.append(loss)
            self.lr_history_.append(self.lr_)

            for start_index in range(0, len(X), batch_size): #make batches, find gradient, update 

                batch_indices = indices[start_index:start_index + batch_size]
        
                X_batch = X[batch_indices]
                y_batch = y[batch_indices]
                B = X_batch.shape[0]

                ## real cooking: 
                y_pred = X_batch @ self.beta_hat
                gradient = -(2/B) * X_batch.T @ (y_batch - y_pred) #the gradient points uphill to the highest slope, so we negate it t point to the smallest/lowest slope okay !!
                self.beta_hat = self.beta_hat - self.lr_ * gradient

            self.n_iter_ = epoch + 1

            if epoch > 0 and abs(self.loss_history_[-2] - self.loss_history_[-1]) < tolerance and batch_size >= n:
                self.stop_reason_ = 'tolerance'
                break

        y_pred = X @ self.beta_hat 
        self.final_loss_ = np.mean((y - y_pred)**2)
        if not np.isfinite(self.final_loss_):
            self.stop_reason_ = 'divergence'


        self.intercept_ = self.beta_hat[0]
        self.coef_ = self.beta_hat[1:]

        return self

    def predict(self, X):
        if self.beta_hat is None:
            raise ValueError(".fit() not called yet, please fit the data")
        X = np.asarray(X, float)
        X = self._add_intercept(X)

        return X @  self.beta_hat

    def residual(self, X, y):
        y = np.asarray(y, float)
        y_pred = self.predict(X)
        resid = y - y_pred
        return resid

    def r2_score(self, X, y):
        y = np.asarray(y, float)

        y_pred = self.predict(X)

        sst = np.sum( (y - np.mean(y)) **2)

        sse = np.sum( (y - y_pred) ** 2 ) 

        if sst == 0.0:
            return 0

        return 1 - (sse/sst)