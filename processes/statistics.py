import pandas as pd
from pathlib import Path

def statistics(
        dataset_folder = "../baseline_dataset",
        samples = 1000
    ):

    print("Loading Dataset...")
    df = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv")).head(samples)

    print("correlation: ", df["density_log"].corr(df["clustering"]))
    print("covariance: ", df["density_log"].cov(df["clustering"]))
    print("density_log min: ", df["density_log"].min())
    print("density_log mean: ", df["density_log"].mean())
    print("density_log max: ", df["density_log"].max())
    print("clustering min: ", df["clustering"].min())
    print("clustering mean: ", df["clustering"].mean())
    print("clustering max: ", df["clustering"].max())