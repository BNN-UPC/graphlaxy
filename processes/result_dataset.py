import random
import numpy as np
from pathlib import Path
import pandas as pd

from utils.rmat import rmat_to_file
from utils.probability import beta_rvs_shifted, beta_rvs_discrete_shifted

def generate_result_dataset(
    from_file = True,
    custom_weights = [1] *8,
    param_file = "../baseline_dataset/parameters.csv", 
    name = "result",
    dataset_folder = '../resulting_dataset',
    dataset_size = 10000,
    edges_between = (1000,1000000),
    multiprocess = False):

    if from_file:
        df = pd.read_csv(param_file)
        params = df[df["name"] == name].iloc[-1][[
                "alfa_a", "beta_a", "alfa_b", "beta_b", "alfa_N", "beta_N"
            ]]
    else:
        params = custom_weights

    print(params)

    alfa_a, beta_a, alfa_b, beta_b, alfa_N, beta_N  = params



    Path(dataset_folder,'graphs').mkdir(parents=True, exist_ok=True)

    parameters = []
    for i in range(0,dataset_size):
        
        E = random.randint(edges_between[0], edges_between[1])
        n_0 = np.floor(np.sqrt(E * 20))
        N = beta_rvs_discrete_shifted(alfa_N, beta_N, n_0, E)

        a = beta_rvs_shifted(alfa_a, beta_a, 0.33, 1)
        b = beta_rvs_shifted(alfa_b, beta_b, max(1 - 2  * a, 0), min(a, 1-a))
        c = 0
        d = 1 - a - b - c

        
        params = {
            "i": i, "N": N, "E": E,
            "a": a, "b": b, "c": c, "d": d
        }

        print("Queue params: ", params)

        parameters.append(params)
    
    if multiprocess:
        from pebble import ProcessPool
        from utils.multiprocess import pebble_timeout_callback

        with ProcessPool() as pool:
            for param in parameters:
                future = pool.schedule(rmat_to_file, 
                    args=(param['N'],param['E'],param['a'],param['b'],param['c'],param['d'],dataset_folder, param['i']), 
                    timeout=300)
                future.add_done_callback(pebble_timeout_callback)
    else:
        for param in parameters:
            rmat_to_file(param['N'],param['E'],param['a'],param['b'],param['c'],param['d'],dataset_folder, param['i'])