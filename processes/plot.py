from argparse import ArgumentError
import random
from statistics import mean
import pandas as pd
import numpy as np

from pathlib import Path
from matplotlib import pyplot as plt

from utils.probability import beta_rvs_shifted
from scipy.stats import beta, uniform
from .bargin import gen_param_grid, gen_weights, gen_metric_grid, grid_bargin, get_grid


def annotate_df(row, ax):
    ax.annotate(row["name"], row[["density_log","clustering"]],
        xytext=(3, -2), 
        textcoords='offset points',
        size=12, 
        color='darkslategrey')

def plot_paramdensity(res, s):
    alfa_a, beta_a, alfa_b, beta_b, alfa_c, beta_c, alfa_N, beta_N = res
    param_list = []
    for _ in range(s):
        a = beta_rvs_shifted(alfa_a, beta_a, 1/3, 1)
        b = beta_rvs_shifted(alfa_b, beta_b, max(0,1-3*a), min(a, 1-a))
        c = beta_rvs_shifted(alfa_c, beta_c, max(0,1-2*a-b), min(a, 1-a-b))
        d = 1-a-b-c
        params = {'a': a, 'b': b, 'c': c, 'd': d}
        param_list.append(params)
    df = pd.DataFrame(param_list)
    plt.figure()
    plt.hist(df, bins=20, label=["a","b", "c","d"], stacked=False, density=True)
    plt.xlabel("value")
    plt.ylabel("density")
    plt.legend()
    plt.xlim(-0,1)
    plt.ylim(0,20)


def plot_clustering_density(df):
    plt.figure()
    plt.hist(df["clustering"], bins=20, density=True)
    index = (0,1)
    plt.plot(index, uniform.pdf(index), label='Uniform')
    plt.ylim(0,10)
    plt.legend()
    plt.xlabel("clustering")
    plt.ylabel("denisty")


def plot_dlog_density(df):
    plt.figure()
    plt.hist(df["density_log"], bins=20, density=True)
    index = (-5.5,0)
    plt.plot(index, uniform.pdf(index, loc=-5.5, scale =5.5), label='Uniform')
    plt.ylim(0,0.5)
    plt.legend()
    plt.xlabel("Dlog")
    plt.ylabel("denisty")

def plot_sample_paramdist(res):
    alfa_a, beta_a, alfa_b, beta_b,alfa_c, beta_c, alfa_N, beta_N  = res
    plt.figure()
    index = np.arange(0,1, 0.01)
    plt.plot(index, beta.pdf(index,alfa_a, beta_a), label='a')
    plt.plot(index, beta.pdf(index,alfa_b, beta_b), label='b')
    plt.plot(index, beta.pdf(index,alfa_c, beta_c), label='c')
    plt.plot(index, beta.pdf(index,alfa_N, beta_N), label='N')
    plt.xlabel("value (before shifting and scaling)")
    plt.ylabel("density")
    plt.legend()


def plot_sample_grid(df):
    ax= df.plot.scatter("density_log","clustering", c="weight_log", colormap='magma')
    grid = get_grid()
    for c in grid[0]:
        ax.plot([-5.5, 0], [c, c], color = 'green', linestyle = '--', linewidth = 0.5)
    for d in grid[1]:
        ax.plot([d, d], [0, 1], color = 'green', linestyle = '--', linewidth = 0.5)

def plot_sample_params(df):
    ax= df.plot.scatter("NE","diff", c="weight_log", colormap='magma') # c="gray")
    #sample.plot.scatter("NE","diff", ax = ax)
    plt.xlabel("N / E")
    plt.ylabel("a - d")

def plot_param_clustering(df):
    df.plot.scatter("NE","diff", c="clustering", colormap='magma')
    plt.xlabel("N / E")
    plt.ylabel("a - d")

def plot_fitness_evolution(df, M, params, name):
    param_serie = params[params["name"].str.startswith("{}_".format(name))].copy()
    param_serie["iteration"] = param_serie["name"].str.extract("_(\d+)$").astype(int)
    param_serie["fitness"] = param_serie[
        ["alfa_a", "beta_a", "alfa_b", "beta_b", "alfa_c", "beta_c", "alfa_N", "beta_N"]
    ].apply(lambda row: grid_bargin(df, M)(row), axis=1)

    ax = param_serie.plot("iteration", "fitness", marker="o")
    param_serie.apply(lambda e: 
        ax.annotate(
            "{:.2f}".format(e["fitness"]), 
            e[["iteration", "fitness"]],
            xytext=(-11,6), 
            textcoords='offset points',
            size=8, 
            color='darkslategrey'
        ), axis=1)
    

    
def plot_param_dlog(df):
    df.plot.scatter("NE","diff", c="density_log", colormap='magma')
    plt.xlabel("N / E")
    plt.ylabel("a - d")

def plot_validation(df, df_val):
    ax = df.plot.scatter("density_log","clustering", c="gray")
    df_val.plot.scatter("density_log","clustering", ax = ax)
    plt.xlabel("Dlog")
    plt.xlim(-6,0.01)
    plt.ylim(-0.01,1.01)
    df_val.apply(lambda row: annotate_df(row,ax), axis=1)

def figure_print(show, folder, name, format):
    if not show:
        Path(folder).mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(folder, "{}.{}".format(name,format)))
    
def plot(
    dataset_folder = "../baseline_dataset",
    validation_metrics = "../validation_dataset/dataset_metrics.csv",
    samples = 0,
    show = True,
    format = 'svg',
    output_folder = "../plots/initial",
    plot_selection = ["validation"],
    custom_weights = [1] * 8,
    weight_source = "custom",
    name = "r10"
    ):

    plt.rcParams.update({'font.size': 22})

    if weight_source == "custom":
        weights = custom_weights
    elif weight_source == "initial":
        weights = [1] * 8

    print("Will plot:", plot_selection)
    if set(["sample_grid", "sample_param", "validation", "dlog_density", "clustering_density",
        "fitness_evolution", "param_clustering", "param_dlog"]) & set(plot_selection):
        print("Loading Dataset...")
        df_m = pd.read_csv(Path(dataset_folder, "dataset_metrics.csv"))
        df_d = pd.read_csv(Path(dataset_folder, "dataset_description.csv"))
        df_b = pd.merge(df_m, df_d, on="name")
        df_b = df_b.sample(samples) if samples > 0 else df_b
        df_b["NE"] = df_b["N"] / df_b["E"]
        df_b["diff"] = df_b["a"] - df_b["d"]

        if set(["sample_grid", "sample_param", "fitness_evolution"]) & set(plot_selection):
            print("Generating weights...")
            #sample = gen_sample(df_b, weights, samples)
            m = 10
            gen_param_grid(df_b,0.05)
            gen_metric_grid(df_b, ["clustering", "density_log"], m)
            gen_weights(df_b, weights)
            df_b["weight_log"] = np.log10(df_b["weight"])
            
        if "validation" in plot_selection:
            print("Loading Validation dataset...")
            df_val = pd.read_csv(validation_metrics)
            
        if "fitness_evolution" in plot_selection:
            if name is None:
                raise ArgumentError("Name must be supplied to plot fitness evolution")
            print("Loading optimized_parameters data...")
            params = pd.read_csv(Path(dataset_folder, "optimized_parameters.csv"))

    if "param_dlog" in plot_selection:
        print("Generating plot: param_dlog...")
        plot_param_dlog(df_b)
        figure_print(show, output_folder, "param_dlog", format)

    if "param_clustering" in plot_selection:
        print("Generating plot: param_clustering...")
        plot_param_clustering(df_b)
        figure_print(show, output_folder, "param_clustering", format)

    if "sample_grid" in plot_selection:
        print("Generating plot: sample_grid...")
        plot_sample_grid(df_b)#, sample)
        figure_print(show, output_folder, "grid", format)
        
    if "sample_paramdist" in plot_selection:
        print("Generating plot: sample_paramdist...")
        plot_sample_paramdist(weights)
        figure_print(show, output_folder, "paramdist", format)

    if "sample_param" in plot_selection:
        print("Generating plot: sample_param...")
        plot_sample_params(df_b) #, sample)
        figure_print(show, output_folder, "params", format)

    if "validation" in plot_selection:
        print("Generating plot: validation...")
        plot_validation(df_b, df_val)
        figure_print(show, output_folder, "validation", format)
        
    if "density_param" in plot_selection:
        print("Generating plot: density_param...")
        plot_paramdensity(weights, samples)
        figure_print(show, output_folder, "density_param", format)
        
    if "clustering_density" in plot_selection:
        print("Generating plot: clustering_density...")
        plot_clustering_density(df_b)
        figure_print(show, output_folder, "clustering_density", format)

    if "dlog_density" in plot_selection:
        print("Generating plot: dlog_density...")
        plot_dlog_density(df_b)
        figure_print(show, output_folder, "dlog_density", format)

    if "fitness_evolution" in plot_selection:
        print("Generating plot: fitness_evolution...")
        plot_fitness_evolution(df_b, m*m, params, name)
        figure_print(show, output_folder, "fitness_evolution", format)

    if show:
        print("Showing plots...")
        plt.show()



    