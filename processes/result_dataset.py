import random
import numpy as np
from pathlib import Path
import pandas as pd

from utils.rmat import rmat_to_file
from utils.probability import beta_rvs_shifted, beta_rvs_discrete_shifted

from scipy.stats import dirichlet

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
                "alfa_a","alfa_b", "alfa_c", "alfa_d",
                "alfa_a_2", "alfa_b_2", "alfa_c_2", "alfa_d_2",
                "alfa_N", "beta_N", "selector"
            ]]
    else:
        params = custom_weights

    print(params)

    #alfa_a, alfa_b, alfa_c, alfa_d, alfa_N, beta_N  = params
    alfa_a,alfa_b, alfa_c, alfa_d, \
        alfa_a_2, alfa_b_2, alfa_c_2, alfa_d_2, \
            alfa_N, beta_N, selector = params




    Path(dataset_folder,'graphs').mkdir(parents=True, exist_ok=True)

    parameters = []
    for i in range(0,dataset_size):
        
        E = random.randint(edges_between[0], edges_between[1])
        n_0 = np.floor(np.sqrt(E * 20))
        N = beta_rvs_discrete_shifted(alfa_N, beta_N, n_0, E)

        if random.random() < selector:
            a,b,c,d = dirichlet.rvs((alfa_a, alfa_b ,alfa_c, alfa_d))[0]
        else:
            a,b,c,d = dirichlet.rvs((alfa_a_2, alfa_b_2 ,alfa_c_2, alfa_d_2))[0]


        
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
