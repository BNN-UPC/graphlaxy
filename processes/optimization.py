from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from utils.filesystem import add_to_csv
from .bargin import grid_bargin, gen_metric_grid, gen_param_grid

def store_params(dataset_folder, name, params, i = None):
  if i is not None:
    name = "{}_{}".format(name,i)

  print("{}: {}".format(name, params))

  alfa_a, beta_a, alfa_d, beta_d, alfa_N, beta_N = params
  add_to_csv(Path(dataset_folder, "optimized_parameters.csv"),{
      'name': name, 'iteration': i,
      'alfa_a': alfa_a, 'beta_a': beta_a,
      'alfa_b': alfa_d, 'beta_b': beta_d,
      'alfa_N': alfa_N, 'beta_N': beta_N,
  })
  
def optimize(
        name = 'result',
        dataset_folder = "../baseline_dataset",
        grid_size = 10):

    df_m = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv"))
    df_d = pd.read_csv(Path(dataset_folder, "dataset_description.csv"))
    df = pd.merge(df_m, df_d, on="name")


    m = grid_size
    M = m * m
    gen_metric_grid(df, ["clustering", "density_log"], m)
    gen_param_grid(df)

    i = 1
    def callback(x):
      nonlocal i
      store_params(dataset_folder, name, x, i)
      i += 1

    initial_parameters = [1] * 6
    store_params(dataset_folder, name, initial_parameters, 0)
    res = minimize(grid_bargin(df, M), initial_parameters, bounds=[(1e-32,20)] * 6,
      callback = callback)
    print(res)

    store_params(dataset_folder, name, res["x"])