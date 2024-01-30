import pandas as pd
import networkx as nx
import numpy as np

from pathlib import Path

from utils.filesystem import read_graph, add_to_csv
from scipy.optimize import curve_fit, minimize
from scipy.stats import powerlaw
import powerlaw as pwl



import multiprocessing as mp

lock = mp.Lock()

def _metrics(dataset_folder, row, trials):
    
    G = read_graph(Path(dataset_folder,"graphs", row['name']))
    #Gcc = max(nx.connected_components(G), key=len)
    #G = G.subgraph(Gcc)

    density = nx.density(G)
    clustering = nx.algorithms.approximation.clustering_coefficient.average_clustering(G,trials)
    max_degree =  max([x[1] for x in nx.degree(G)])

    degree_sequence = sorted([d for n, d in G.degree()]) # used for degree distribution and powerlaw test
    degree_hist = np.unique(degree_sequence, return_counts=True)
    degree_sequence_norm =  np.array(degree_sequence) / max(degree_sequence)

    fit = pwl.Fit(degree_sequence)
    degree_pl_slope = fit.power_law.alpha

    with lock:
        add_to_csv(Path(dataset_folder, "dataset_metrics.csv"), {
            'name': row['name'], 'nodes': G.number_of_nodes(), 'edges': G.number_of_edges(),
            'density': density,
            "max_degree": max_degree,
            'density_log': np.log10(density),
            'clustering':  clustering,
            'degree_pl_slope': degree_pl_slope
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

        with ProcessPool(max_workers=15) as pool:
            for _, row in df.iterrows():
                future = pool.schedule(_metrics,
                    args = (dataset_folder, row, clusterig_trails),
                    timeout = 300)
                future.add_done_callback(pebble_timeout_callback)
    else:
        for _, row in df.iterrows():
            _metrics(dataset_folder, row, clusterig_trails)