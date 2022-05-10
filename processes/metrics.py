import pandas as pd
import networkx as nx
import numpy as np

from pathlib import Path

from utils.filesystem import read_graph, add_to_csv

import multiprocessing as mp

lock = mp.Lock()

def _metrics(dataset_folder, row, trials):
    a = row['a']
    b = row['b']
    c = row['c']
    d = 1 - a - b - c
    
    G = read_graph(row['name'])
    #Gcc = max(nx.connected_components(G), key=len)
    #G = G.subgraph(Gcc)

    density = nx.density(G)
    clustering = nx.algorithms.approximation.clustering_coefficient.average_clustering(G,trials)
    max_degree =  max([x[1] for x in nx.degree(G)])

    with lock:
        add_to_csv(Path(dataset_folder, "dataset_metrics.csv"), {
            'name': row['name'], 'nodes': G.number_of_nodes(), 'edges': G.number_of_edges(),
            'density': density,
            "max_degree": max_degree,
            'density_log': np.log10(density),
            'clustering':  clustering
        })
    return row['name']


def calculate_metrics(
        dataset_folder = "../baseline_dataset",
        clusterig_trails = 1000,
        multiprocess = False):
    df = pd.read_csv(Path(dataset_folder, 'dataset_description.csv'))
    if multiprocess:
        from pebble import ProcessPool
        from utils.multiprocess import pebble_timeout_callback

        with ProcessPool() as pool:
            for _, row in df.iterrows():
                future = pool.schedule(_metrics,
                    args = (dataset_folder, row, clusterig_trails),
                    timeout = 300)
                future.add_done_callback(pebble_timeout_callback)
    else:
        for _, row in df.iterrows():
            _metrics(dataset_folder, row, clusterig_trails)