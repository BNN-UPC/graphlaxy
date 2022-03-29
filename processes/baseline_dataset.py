import random
import numpy as np
from pathlib import Path
from utils.rmat import rmat_to_file

def generate_baseline(
    dataset_folder = "../baseline_dataset", 
    dataset_size = 10000,
    edges_between = (1000,1000000),
    multiprocess = False):

    Path(dataset_folder,'graphs').mkdir(parents=True, exist_ok=True)

    parameters = []
    for i in range(0,dataset_size):
        E = random.randint(edges_between[0],edges_between[1])

        n_0 = np.floor(np.sqrt(E * 2))
        N_r = (n_0, E + 1)
        N = int(np.floor(random.uniform(N_r[0],N_r[1])))

        a = random.uniform(0.25, 1)
        b = random.uniform((1-a)/3, min(a, 1-a))
        c = random.uniform((1-a-b)/2, min(b, 1-a-b))
        d = 1-a-b-c

        parameters.append({
            "i": i, "N": N, "E": E,
            "a": a, "b": b, "c": c, "d": d
        })

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