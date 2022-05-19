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

  alfa_a, beta_a, alfa_b, beta_b, alfa_c, beta_c, alfa_N, beta_N = params
  add_to_csv(Path(dataset_folder, "optimized_parameters.csv"),{
      'name': name, 'iteration': i,
      'alfa_a': alfa_a, 'beta_a': beta_a,
      'alfa_b': alfa_b, 'beta_b': beta_b,
      'alfa_c': alfa_c, 'beta_c': beta_c,
      'alfa_N': alfa_N, 'beta_N': beta_N,
  })
  
def optimize(
        name = 'result',
        dataset_folder = "../baseline_dataset",
        grid_size = 10):

    df_m = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv"))
    df_d = pd.read_csv(Path(dataset_folder, "dataset_description.csv"))
    df = pd.merge(df_m, df_d, on="name")
    df[df["density_log"] < -1]


    m = grid_size
    M = m * m
    gen_metric_grid(df, ["clustering", "density_log"], m)
    gen_param_grid(df)

    i = 1
    def callback(x):
      nonlocal i
      store_params(dataset_folder, name, x, i)
      i += 1

    initial_parameters = [1] * 8
    store_params(dataset_folder, name, initial_parameters, 0)
    res = minimize(grid_bargin(df, M), initial_parameters, bounds=[(1e-32,100)] * 8,
      tol = 0.01, callback = callback)
    print(res)

    store_params(dataset_folder, name, res["x"])