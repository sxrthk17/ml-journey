import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

def residual_fitted_plot(y_pred, residuals):
    plt.figure(figsize=(6,5))
    plt.scatter(y_pred, residuals, color='red', alpha=0.7)
    plt.title("Residual Fitter Plot")
    plt.axhline(y=0, ls='--', color='black')
    plt.tight_layout()
    plt.show()

def plot_qq(residual, title="Q-Q Plot"):
    residual = np.asarray(residual, float)
    # residual_sorted = np.sort(residual) No need to sort it here

    plt.figure(figsize=(6, 5))
    stats.probplot(residual, dist="norm", plot=plt)
    plt.title(f"{title}")
    plt.xlabel("Theoritical Quantiles")
    plt.ylabel("Ordered values")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def spread_plot(predictions, errors, title="Spread Plot", ylabel="Error"):
    predictions = np.asarray(predictions, float)
    errors = np.asarray(errors, float)

    if predictions.shape[0] != errors.shape[0]:
        raise ValueError("Length of Predictions and Errors must be same for plot!!")

    spread_df = pd.DataFrame({"prediction":predictions,
                            "errors":errors})

    spread_df['pred_bin'] = pd.qcut(spread_df['prediction'], q=10)
    bin_summary = spread_df.groupby('pred_bin', observed=False)['errors'].mean().reset_index()

    bin_midpoints = bin_summary['pred_bin'].apply(lambda x: x.mid)

    plt.figure(figsize=(6,5))
    plt.scatter(predictions, errors, color='salmon', label='Indiviual points')
    plt.plot(bin_midpoints, bin_summary['errors'], marker='o', color='black', linewidth=2, label='Binned Mean Error Trend')
    plt.title(title)
    plt.xlabel("Predicted Values: ($\hat{y}$)")
    plt.ylabel(f"{ylabel}")
    plt.legend()
    plt.show()

def residual_by_predictors_plot(X, residual):
    if X.shape[0] != len(residual):
        raise ValueError("Length of X and Residual must be same !! ")

    if isinstance(X, pd.DataFrame):
        for i in range(X.shape[1]):

            plt.figure(figsize=(5,5))
            plt.scatter(X.iloc[:, i], residual, color='lightblue')
            plt.title(f"{X.columns[i]} vs Residual Plot")
            plt.xlabel(f"{X.columns[i]}")
            plt.ylabel("Residuals")
            plt.tight_layout()
            plt.show()

    elif isinstance(X, np.ndarray):
        for i in range(X.shape[1]):

            plt.figure(figsize=(5,5))
            plt.scatter(X[:, i], residual, color='lightblue')
            plt.title(f"Predictor vs Residual Plot")
            plt.xlabel(f"Predictor")
            plt.ylabel("Residuals")
            plt.tight_layout()
            plt.show()

def average_residual_spread_by_hour(hr_val, residual):
    hourly_summary = (
        pd.DataFrame({'hr': hr_val, 'residual': residual})
        .groupby('hr').agg(mean_residual=('residual', 'mean'),
                        std_residual=('residual', 'std')).reset_index()
    )

    
    plt.figure(figsize=(12, 6))

    plt.plot(
    hourly_summary['hr'],
    hourly_summary['mean_residual'],
    marker='o',
    color='crimson',
    linewidth=2,
    label='Mean Residual',)

    plt.fill_between(
        hourly_summary['hr'],
        hourly_summary['mean_residual'] - hourly_summary['std_residual'],
        hourly_summary['mean_residual'] + hourly_summary['std_residual'],
        color='crimson',
        alpha=0.2,
        label='±1 Std Dev Spread',
    )

    plt.axhline(
        0, color='black', linestyle='--', linewidth=1, label='Zero Error Line'
    )

    plt.title(
        'Residual Spread by Hour of Day (One-Hot Model Validation Set)',
        fontsize=12,
        fontweight='bold',
    )
    plt.xlabel('Hour of Day', fontsize=10)
    plt.ylabel('Residual (Actual - Predicted)', fontsize=10)
    plt.xticks(range(24))
    plt.legend()
    plt.tight_layout()
    plt.show()