from pathlib import Path
from jmetal.core.quality_indicator import *
from solution import GraphSolution
from solution_parser import read_solutions_objectives, read_solutions_variables
from scipy.stats import kstest
from greedy_algorithms import max_conn_greedy, min_cost_greedy
from utils import *
from jmetal.util.solution import (
    read_solutions,
    print_function_values_to_file,
    print_variables_to_file,
)
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.lab.visualization import Plot
from pandas import DataFrame
import matplotlib.pyplot as plt

""" Reads a reference front from a file.

:param filename: File path where the front is located.
"""

all_executions_statistics = {}

instances = [
    (NEIGHBORHOODS_GRAPH, 40, "NEIGHBORHOODS_GRAPH_CENTRAL_40"),
    (FIRST_31_GRAPH, 15, "FIRST_31_GRAPH_CENTRAL_15"),
    (FIRST_31_GRAPH, 20, "FIRST_31_GRAPH_CENTRAL_20"),
    (FIRST_31_GRAPH, 25, "FIRST_31_GRAPH_CENTRAL_25"),
    (FIRST_31_GRAPH, 30, "FIRST_31_GRAPH_CENTRAL_30")
]

algorithms = ["NSGAII", "SPEA2"]

def statistics(data):
    np_data = np.array(data)
    return np.mean(np_data), np.std(np_data)

def nadir(pareto):
    data = np.array(pareto)
    return [data[:,0].max(), data[:,1].max()]

def sort_by_run(all_executions_values, n_run):
    n_values = []
    for key in all_executions_values:
        n_values.append((key, all_executions_values[key][n_run]))
    n_values = sorted(n_values, key=lambda x: x[1], reverse=True)
    return n_values

def ranking_in(positions, key):
    element = [element for element in positions if element[0] == key][0]
    return positions.index(element)


def rank_test(all_executions_values):
    key_ranks = {}

    for key in all_executions_values.keys():
        key_ranks[key] = 0

    for n_run in range(30):
        sorted_n_run = sort_by_run(all_executions_values, n_run)
        for key in all_executions_values.keys():
            key_ranks[key] += ranking_in(sorted_n_run, key)

    for key in all_executions_values.keys():
        key_ranks[key] = key_ranks[key] / 30

    return key_ranks

def evaluation_statistical_analysis():
    all_instances_rank_test = { 'NSGAII': 0, 'SPEA2': 0}
    all_executions_values = {}
    for instance in instances:
        instance_name = instance[2]
        reference_pareto = read_solutions_objectives(f'evaluation/FUN.PARETO_DFOM_SPEA2-{instance_name}')
        hypervolume = HyperVolume(nadir(reference_pareto))
        pareto_hypervolume = hypervolume.compute(reference_pareto)
        all_executions_values[instance_name] = {}
        all_executions_statistics[instance_name] = {}
        for algorithm in algorithms:
            all_executions_values[instance_name][algorithm] = []
            all_executions_statistics[instance_name][algorithm] = []
            for n in range(30):
                filename_fun = f'evaluation/fun/FUN.{instance_name}-{algorithm}-RUN_{n}'
                execution_solutions = read_solutions_objectives(filename_fun)
                execution_hypervolume = hypervolume.compute(execution_solutions)
                all_executions_values[instance_name][algorithm].append(execution_hypervolume / pareto_hypervolume)
            all_executions_statistics[instance_name][algorithm] = statistics(all_executions_values[instance_name][algorithm])
            print("KS: ",kstest(all_executions_values[instance_name][algorithm], "norm"))
        print(all_executions_statistics)
        print("Instance: ", instance_name)
        print(f"Rank Test by Instance {instance_name}: ")
        rank_test_by_instance = rank_test(all_executions_values[instance_name])
        for algorithm in algorithms:
            all_instances_rank_test[algorithm] += rank_test_by_instance[algorithm]
        print(rank_test(all_executions_values[instance_name]))
    for algorithm in algorithms:
        print(f"Rank Promedio en Todas las instancias de {algorithm}: ", all_instances_rank_test[algorithm] / 5)


def greedy_comparison():
    greedy_values = {}
    for instance in instances:
        instance_name = instance[2]
        greedy_values[instance_name] = {"max_conn": [], "min_cost": []}
        greedy_values[instance_name]["max_conn"] = max_conn_greedy(instance[0], instance[1])
        greedy_values[instance_name]["min_cost"] = min_cost_greedy(instance[0], instance[1])
        for algorithm in algorithms:
            filename_fun = f'evaluation/alg_pareto/FUN.PARETO_DFOM_{algorithm}-{instance_name}'
            pareto_front = read_solutions(filename_fun)
            df = Plot.get_points(pareto_front)[0].rename(columns={0: "x", 1: "y"})
            df.plot(x = 'x', y = 'y', kind = "scatter", grid = True, legend = True, xlabel = 'cost', ylabel = 'connectivity', title = f'{instance_name}: Greedy vs {algorithm}')
            print("val", greedy_values[instance_name]["min_cost"])
            plt.scatter(greedy_values[instance_name]["min_cost"][0], greedy_values[instance_name]["min_cost"][1], c="red")
            plt.scatter(greedy_values[instance_name]["max_conn"][0], greedy_values[instance_name]["max_conn"][1], c="blue")
            plt.show()


def get_algorithm_pareto():
    for instance in instances:
        instance_name = instance[2]
        for algorithm in algorithms:
            all_solutions=[]
            for n in range(30):
                filename_fun = f'evaluation/fun/FUN.{instance_name}-{algorithm}-RUN_{n}'
                all_solutions += read_solutions(filename_fun)

            reference_pareto_front = get_non_dominated_solutions(all_solutions)
            print_function_values_to_file(reference_pareto_front, f'evaluation/alg_pareto/FUN.PARETO_DFOM_{algorithm}-{instance_name}')
            print_variables_to_file(reference_pareto_front, f'evaluation/alg_pareto/VAR.PARETO_DFOM_{algorithm}-{instance_name}')

if __name__ == "__main__":
    # print(all_executions_statistics)
    # print(all_executions_values)
    # population_adjustment()
    # evaluation_statistical_analysis()
    greedy_comparison()



