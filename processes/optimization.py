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
   #   'alfa_a': alfa_a, 'beta_a': beta_a,
   #   'alfa_b': alfa_b, 'beta_b': beta_b,
   #   'alfa_c': alfa_c, 'beta_c': beta_c,
     'alfa_a': alfa_a, 'alfa_b': alfa_b,'alfa_c': alfa_c,'alfa_d': alfa_d,
      'alfa_N': alfa_N, 'beta_N': beta_N, 'f': f
  })
  
def optimize(
        name = 'result',
        dataset_folder = "../baseline_dataset",
        grid_size = 10,
        custom_weights = [2] * 6):

    df_m = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv"))
    df_d = pd.read_csv(Path(dataset_folder, "dataset_description.csv"))
    df = pd.merge(df_m, df_d, on="name")
    df[df["density_log"] < -1]


    m = grid_size
    M = m * m
    gen_metric_grid(df, ["clustering", "density_log"], m)
    gen_param_grid(df)

    i = 1
    def callback(x, f, acc):
      nonlocal i
      print(x)#,f ,acc)
      #if acc:
      store_params(dataset_folder, name, x, i,None)
      i += 1

    store_params(dataset_folder, name, custom_weights, 0)
    #res = basinhopping(grid_bargin(df, M), custom_weights, callback = callback, stepsize=5
    #                  , interval=5, niter=1000, T = 0.1, minimizer_kwargs={"method":"COBYLA","options":{"maxiter":50, "disp":True, "eps": 1e-2}})
    res = minimize(grid_bargin(df, M), custom_weights, method="COBYLA", tol= 1e-2, options={"disp":True}) # "eps": 1e-2
    print(res)

    store_params(dataset_folder, name, res["x"])