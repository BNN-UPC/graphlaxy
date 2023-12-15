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
  add_to_csv(Path(dataset_folder, "optimized_parameters.csv"),{
      'name': name, 'iteration': i,
     'alfa_a': alfa_a, 'alfa_b': alfa_b,'alfa_c': alfa_c,'alfa_d': alfa_d,
      'alfa_N': alfa_N, 'beta_N': beta_N, 'f': f
  })
  
def optimize(
        name = 'result',
        dataset_folder = "../baseline_dataset",
        grid_size = 10,
        precision = 0.05,
        custom_weights = None):

    df_m = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv"))
    df_d = pd.read_csv(Path(dataset_folder, "dataset_description.csv"))
    df = pd.merge(df_m, df_d, on="name")
    df[df["density_log"] < -1]


    m = grid_size
    M = m * m
    gen_metric_grid(df, ["clustering", "density_log"], m)
    gen_param_grid(df, precision)

    i = 1
    def callback(x):
      nonlocal i
      print(x)
      store_params(dataset_folder, name, x, i,None)
      i += 1

    if custom_weights == None:
      f_min = 0
      for i in range(100):
        custom_weights_i = np.random.rand(6) * 5
        f = grid_bargin(df, M)(custom_weights_i)
        if f < f_min:
          f_min = f
          custom_weights  = custom_weights_i
          print(custom_weights, f)

    store_params(dataset_folder, name, custom_weights, 0)
    res = minimize(grid_bargin(df, M), custom_weights, method="COBYLA", tol= 1e-3, options={"disp":True}) # "eps": 1e-2
    print(res)

    store_params(dataset_folder, name, res["x"])
