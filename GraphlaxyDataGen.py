#!/usr/bin/env python

import argparse
import sys

class Graphlaxy(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Tool used to create synthetic graph datasets using \'Nash Bargin Scheme\' optimization.',
            usage='''gdg <command> [<args>]

The available commands are:
    optimization         Create a baseline dataset and optimize the parameters.
    generate    Using the fitted parameters generate a synthetic graph dataset.
    plots       Generate plots showing different characteristics of the baseline, sampled, and final datasets. 
    statistics  Print some basic statistics of target dataset
''')
        parser.add_argument('command', help='Subcommand to run')
        commands = {
            "optimization":self.optimization, 
            "generate":self.generate, 
            "plots": self.plot,
            "statistics": self.statistics
        }
        args = parser.parse_args(sys.argv[1:2])
        if not args.command in commands:
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        commands[args.command]()

    
    def optimization(self):
        parser = argparse.ArgumentParser(description = "Steps for the optimization.",
        usage='''gdg optimiation <subcommand> [<args>]

The available subcommands are:
    baseline    Only creates the baseline dataset
    metrics     Calculate the metrics of a dataset
    optimize    Use sampling and the Powell method with cooperative bargaining to optimize the input RMat parameters

*************************************
To run the full optimization in steps:
    First, create the baseline dataset, then take the metrics and finally optimize the parameters.''')


        parser.add_argument('subcommand', help='Subcommand to run')
        
        commands = {
            "baseline":self.baseline, 
            "metrics":self.metrics, 
            "optimize": self.optimize
            }
        args = parser.parse_args(sys.argv[2:3])
        if not args.subcommand in commands:
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        commands[args.subcommand]()

    def generate(self):
        parser = argparse.ArgumentParser(description = "Using the fitted parameters generate a synthetic graph dataset.")

        parser.add_argument('-f', "--folder", metavar = "str", type = str,
                            help = "Folder where to generate the dataset.", default= "../result_dataset")
        parser.add_argument('-s', "--dataset-size", metavar = "int", type = int,
                            help = "The size of the dataset to generate.", default= 100)
        parser.add_argument('-e', "--edges-between", nargs = 2, metavar = "int", type = int,
                            help = "The min and max vallue the edges argument can take.", default= (100000, 2000000))
        parser.add_argument('-m', '--multiprocess', action="store_true", help = "Add to take advantage of multiple cores.")

        parser.add_argument('-w', "--custom-weights", nargs = 6, metavar = "float", type = float,
                            help = "List of waights for the beta distributions.", 
                            default= [2.473828998367313,0.8392523785309522,0.5058416664822544,0.23394588882493786,0.28724838342218206,2.5188610470866606])


        
        parser.add_argument('-F', '--from-file', action="store_true", 
            help = "Use a stored set of waights. Use with --parameters-file and --name parameters to indicate where to get the waights from. By seting this parameters the paramete --custom-weights gets disabled.")
        parser.add_argument('-p', "--parameters-file", metavar = "str", type = str,
                            help = "File where the parameters are", default= "../baseline_dataset/optimized_parameters.csv")
        parser.add_argument('-n', "--name", metavar = "str", type = str,
                            help = "An id for the parameters.", default= "result")
        args = parser.parse_args(sys.argv[2:])

        from processes.result_dataset import generate_result_dataset

        generate_result_dataset(args.from_file, args.custom_weights, args.parameters_file, args.name, args.folder, args.dataset_size, args.edges_between, args.multiprocess)


    def statistics(self):
        parser = argparse.ArgumentParser(description = "Calculate some statistics over a dataset.")
        
        parser.add_argument('-f', "--folder", metavar = "str", type = str,
                            help = "Folder where the dataset to analize was generated.", default= "data/validation_dataset")
        parser.add_argument('-s', "--sample-size", metavar = "int", type = int,
                            help = "The size of the sample.", default= 1000)

        args = parser.parse_args(sys.argv[2:])
        from processes.statistics import statistics
        statistics(args.folder, args.sample_size)

    def plot(self):
        parser = argparse.ArgumentParser(description = "Some plots to analyze the results.")

        parser.add_argument('-f', "--folder", metavar = "str", type = str,
                            help = "Folder where the dataset to analize was generated.", default= "../baseline_dataset")
        parser.add_argument('-v', "--validation-metrics", metavar = "str", type = str,
                            help = "File where the validation metrics are.", default= "data/validation_dataset/dataset_metrics.csv")
        parser.add_argument('-F', "--format", metavar = "str", type = str,
                            help = "Format to save generated images in.", default= "svg")
        parser.add_argument('-o', "--output-folder", metavar = "str", type = str,
                            help = "Folder where to save plots.", default= "../plots")
        parser.add_argument('-s', "--sample-size", metavar = "int", type = int,
                            help = "The size of the sample.", default= 1000)
        parser.add_argument('-sh', '--show-plots', action="store_true", help = "Show plots instead of saving them.")
        choices = ["fitness_evolution", "clustering_density", "dlog_density", "density_param", "validation", "param_dlog", "param_clustering", "sample_param", "sample_paramdist", "sample_grid"]
        default = ["sample_param", "sample_paramdist", "sample_grid"]
        parser.add_argument('-p', "--plot-selection", nargs = '+', metavar = "str", type = str,
                            help = "Selects the plots to make. Posible values: {}".format(choices), default= default,
                            choices= choices)
        parser.add_argument('-w', "--custom-weights", nargs = 6, metavar = "float", type = float,
                            help = "List of waights for the beta distributions.", 
                            default= ((1,1,1,1,1,1)))
        choices = ["custom", "initial"]
        parser.add_argument('-ws', "--weight-source", metavar = "str", type = str,
                            help = "Where to get the waights used for the plot from. Posible values: {}".format(choices), default= "custom",
                            choices= choices)
        parser.add_argument('-n', "--name", metavar = "str", type = str,
                            help = "Name of the params to use for the fitness_evolution.", default= "result")
        

        args = parser.parse_args(sys.argv[2:])
        from processes.plot import plot
        plot(args.folder, args.validation_metrics, args.sample_size, args.show_plots, args.format, args.output_folder, args.plot_selection, args.custom_weights, args.weight_source, args.name)


    def baseline(self):
        parser = argparse.ArgumentParser(description = "Creates the baseline dataset.")

        parser.add_argument('-f', "--folder", metavar = "str", type = str,
                            help = "Folder where to generate the baseline dataset.", default= "../baseline_dataset")
        parser.add_argument('-s', "--dataset-size", metavar = "int", type = int,
                            help = "The size of the baseline dataset.", default= 10000)
        parser.add_argument('-e', "--edges-between", nargs = 2, metavar = "int", type = int,
                            help = "The min and max vallue the edges argument can take.", default= (100000, 2000000))
        parser.add_argument('-m', '--multiprocess', action="store_true", help = "Add to take advantage of multiple cores.")
        
        args = parser.parse_args(sys.argv[3:])
        from processes.baseline_dataset import generate_baseline
        generate_baseline(args.folder, args.dataset_size, args.edges_between, args.multiprocess)



    def metrics(self):
        parser = argparse.ArgumentParser(description = "Calculate metrics of each graph in a dataset.")

        parser.add_argument('-f', "--folder", metavar = "str", type = str,
                            help = "Folder where the dataset is.", default= "../baseline_dataset")
        parser.add_argument('-t', "--clustering-trials", metavar = "int", type = int,
                            help = "Number of trials used to approximate the clustering cooeficient.", default=1000)
        parser.add_argument('-m', '--multiprocess', action="store_true", help = "Add to take advantage of multiple cores.")
        
        args = parser.parse_args(sys.argv[3:])
        from processes.metrics import calculate_metrics
        calculate_metrics(args.folder, args.clustering_trials, args.multiprocess)


    def optimize(self):
        parser = argparse.ArgumentParser(description = "Calculate metrics of each graph in a dataset.")

        parser.add_argument('-n', "--name", metavar = "str", type = str,
                            help = "An id for the result.", default= "result")
        parser.add_argument('-f', "--folder", metavar = "str", type = str,
                            help = "Folder where the dataset is.", default= "../baseline_dataset")
        parser.add_argument('-g', "--grid-size", nargs='+', metavar = "int", type = int,
                            help = "The number of rows and columns the grid has.", default=[4,8])
        parser.add_argument('-p', "--precision", metavar = "float", type = float,
                            help = "Precition on the metric space.", default=0.05)
        parser.add_argument('-w', "--custom-weights", nargs = 6, metavar = "float", type = float,
                            help = "Initial weights for optimization.", 
                            default= [1]*6)
        
        args = parser.parse_args(sys.argv[3:])

        from processes.optimization import optimize
        optimize(args.name, args.folder, args.grid_size, args.precision, args.custom_weights)


if __name__ == "__main__":
    Graphlaxy()
