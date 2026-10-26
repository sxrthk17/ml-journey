import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def residual_fitted_plot():
    pass

def plot_qq(residual, title="Q-Q Plot"):
    residual_sorted = np.sort(residual)

    plt.figure(figsize=(6, 5))
    stats.probplot(residual_sorted, dist="norm", plot=plt)
    plt.title(f"{title}")
    plt.xlabel("Theoritical Quantiles")
    plt.ylabel("Ordered values")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()