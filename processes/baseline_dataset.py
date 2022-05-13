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
        n_0 = np.floor(np.sqrt(E * 20))
        N = int(np.floor(random.uniform(n_0, E+1)))


        a = random.uniform(0.25, 1)
        c = b = random.uniform(max((1 - 2  * a)/2, 0),min(a,(1-a)/2))
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