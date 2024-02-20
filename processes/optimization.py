from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize, basinhopping

from utils.filesystem import add_to_csv
from .bargin import grid_bargin, gen_metric_grid, gen_param_grid

def store_params(dataset_folder, name, params, i = None, f = None):
  if i is not None:
    name = "{}_{}".format(name,i)

  print("{}: {}".format(name, params))

  alfa_a,alfa_b, alfa_c, alfa_d, alfa_N, beta_N = params
  data = {
      'name': name, 'iteration': i,
     'alfa_a': alfa_a, 'alfa_b': alfa_b,'alfa_c': alfa_c,'alfa_d': alfa_d,
      'alfa_N': alfa_N, 'beta_N': beta_N, 'f': f
  }
  add_to_csv(Path(dataset_folder, "optimized_parameters.csv"), data)
  
def optimize(
        name = 'result',
        dataset_folder = "../baseline_dataset",
        grid_size = 10,
        precision = 0.05,
        custom_weights = None):

    df_m = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv"))
    df_d = pd.read_csv(Path(dataset_folder, "dataset_description.csv"))
    df = pd.merge(df_m, df_d, on="name")

    ms = grid_size
    gen_metric_grid(df, ["clustering", "degree_slope_inverse"], ms)
    gen_param_grid(df, precision)

    i = 1
    def callback(x):
      nonlocal i
      print(x)
      store_params(dataset_folder, name, x, i, grid_bargin(df, ms)(x))
      i += 1

    store_params(dataset_folder, name, custom_weights,0, grid_bargin(df, ms)(custom_weights))
    res = minimize(grid_bargin(df, ms), custom_weights, method="COBYLA", tol= 1e-3, options={"disp":True}) # "eps": 1e-2
    print(res)

    store_params(dataset_folder, name, res["x"])
