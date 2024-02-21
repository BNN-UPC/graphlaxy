import pandas as pd
from pathlib import Path
from scipy import stats
from sklearn.preprocessing import minmax_scale

def statistics(
        dataset_folder = "../baseline_dataset",
        samples = 1000
    ):

    print("Loading Dataset...")
    df = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv")).head(samples)

    print("correlation: ", df["degree_slope_inverse"].corr(df["clustering"]))
    print("covariance: ", df["degree_slope_inverse"].cov(df["clustering"]))
    print("degree_slope_inverse min: ", df["degree_slope_inverse"].min())
    print("degree_slope_inverse mean: ", df["degree_slope_inverse"].mean())
    print("degree_slope_inverse max: ", df["degree_slope_inverse"].max())
    print("clustering min: ", df["clustering"].min())
    print("clustering mean: ", df["clustering"].mean())
    print("clustering max: ", df["clustering"].max())

    df["degree_slope_inverse_norm"] = minmax_scale(df["degree_slope_inverse"])
    # Perform Kolmogorov-Smirnov test
    ks_statistic, p_value = stats.kstest(df["clustering"], 'uniform')
    print(f"Clustering Statistic: {ks_statistic}, p-value: {p_value}")
    ks_statistic, p_value = stats.kstest(df["degree_slope_inverse_norm"], 'uniform')
    print(f"Density Statistic: {ks_statistic}, p-value: {p_value}")
