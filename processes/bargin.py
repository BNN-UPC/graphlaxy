import numpy as np
import pandas as pd
from scipy.stats import dirichlet

from utils.probability import beta_cdf_interval, beta_cdf_mean, beta_cdf_mean_2d

def get_grid(m=10,
        limits = [(0,1),(-6,-1)]):
    
    block0 = np.linspace(limits[0][0], limits[0][1], m + 1)
    block1 = np.linspace(limits[1][0], limits[1][1], m + 1)
    return [block0, block1]



def gen_metric_grid(df, metrics, m):
    if len(metrics) != 2:
        raise NotImplementedError("Only implemented 2D Grid. Please send only one pair of metrics.")

    blocks = get_grid(m)

    df["metric_bucket_1"] = pd.cut(df[metrics[0]], blocks[0], labels=list(range(m)), include_lowest =True)
    df["metric_bucket_2"] = pd.cut(df[metrics[1]], blocks[1], labels=list(range(m)), include_lowest =True)

def interval_b(a):
    return (max(0,1-3*a), min(a, 1-a))

def interval_c(a,b):
    return (max(0,1-2*a-b), min(a, 1-a-b))


def interval_c_mean(a, b):
    a_maen = (a.right + a.left) /2
    b_mean = (b.right + b.left) /2
    return interval_c(a_maen, b_mean)

def interval_c_leftleft(a,b):
    return interval_c(a.left, b.left)
    
def interval_c_leftright(a,b):
    return interval_c(a.left, b.right)

    
def interval_c_rightleft(a,b):
    return interval_c(a.right, b.left)

    
def interval_c_rightright(a,b):
    return interval_c(a.right, b.right)

def interval_b_mean(a):
    a_maen = (a.right + a.left) /2
    return interval_b(a_maen)
    

def interval_b_left(a):
    return interval_b(a.left)
    
def interval_b_right(a):
    return interval_b(a.right)
    

def gen_param_grid(df, precision):
    intervals = np.arange(0,1.001,precision)
    df["NE"] = (df["N"] - np.floor(np.sqrt(df["E"] * 20))) / df["E"]
    df["a_bucket"] = pd.cut(df["a"], intervals, include_lowest =True)
    df["b_bucket"] = pd.cut(df["b"], intervals, include_lowest =True)
    df["c_bucket"] = pd.cut(df["c"], intervals, include_lowest =True)
    df["d_bucket"] = pd.cut(df["d"], intervals, include_lowest =True)
    df["NE_bucket"] = pd.cut(df["NE"], intervals, include_lowest =True)
    df["param_bucket_count"] = df.groupby(['a_bucket', 'b_bucket', 'c_bucket', 'NE_bucket'])[['a_bucket']].transform('count')


def gen_weights(df, res):
    alfa_a, alfa_b ,alfa_c, alfa_d, alfa_N, beta_N  = res
    approx_cdf_trials = 10000
    gen = pd.DataFrame(dirichlet.rvs((alfa_a, alfa_b ,alfa_c, alfa_d), approx_cdf_trials), columns=['a','b','c','d'])

    weights = df.apply(lambda row: (len(gen[gen['a'].between(row['a_bucket'].left,row['a_bucket'].right) & 
                                           gen['b'].between(row['b_bucket'].left,row['b_bucket'].right)& 
                                           gen['c'].between(row['c_bucket'].left,row['c_bucket'].right)& 
                                           gen['d'].between(row['d_bucket'].left,row['d_bucket'].right)
                                           ].index) / approx_cdf_trials) * 
        beta_cdf_interval(row['NE_bucket'],alfa_N, beta_N, (0, 1)) / row["param_bucket_count"], axis=1)

    weights[weights < 0] = 0
    df["weight"] = weights

def grid_bargin(df, M):

    def _grid_bargin(params):
        if any(x <= 0 for x in params):
            return 1

        gen_weights(df, params)

        total = df["weight"].sum()
        buckets = df[(df["metric_bucket_1"] != np.NaN)  & (df["metric_bucket_2"] != np.NaN)].groupby(["metric_bucket_1", "metric_bucket_2"])
        bucket_prob = buckets["weight"].sum() / total


        bargin = - sum(np.log2( 1 + (M-1) * bucket_prob)) / M
        print(params, bargin)
        return bargin
    
    return _grid_bargin

