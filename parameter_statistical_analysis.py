from pathlib import Path
from jmetal.core.quality_indicator import *
from solution import GraphSolution
from solution_parser import read_solutions_objectives, read_solutions_variables
from scipy.stats import kstest

""" Reads a reference front from a file.

:param filename: File path where the front is located.
"""

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

def mutcross_adjustment():
    mutation_probabilities = [0.001, 0.01, 0.1]
    crossover_probabilities = [0.5, 0.75, 1]
    all_executions_values = {}
    reference_pareto = read_solutions_objectives('reference/FUN.PARETO_DFOM_SPEA2')
    hypervolume = HyperVolume(nadir(reference_pareto))
    pareto_hypervolume = hypervolume.compute(reference_pareto)

    for mutation_probability in mutation_probabilities:
        for crossover_probability in crossover_probabilities:
            key = f'MUT_{mutation_probability}-CROSS_{crossover_probability}'
            all_executions_values[key] = []
            for n in range(30):
                filename_fun = f'data/fun/FUN.MUT_{mutation_probability}-CROSS_{crossover_probability}-RUN_{n}'
                execution_solutions = read_solutions_objectives(filename_fun)
                execution_hypervolume = hypervolume.compute(execution_solutions)
                all_executions_values[key].append(execution_hypervolume / pareto_hypervolume)
            # print("KS: ",kstest(all_executions_values[key], "norm"))
    print(rank_test(all_executions_values))

def population_adjustment():
    population_sizes = [50, 124, 200]
    all_executions_values = {}
    reference_pareto = read_solutions_objectives('population_size_adjustment/reference/FUN.PARETO_DFOM_SPEA2')
    hypervolume = HyperVolume(nadir(reference_pareto))
    pareto_hypervolume = hypervolume.compute(reference_pareto)

    for population_size in population_sizes:
            key = f'POP_{population_size}'
            all_executions_values[key] = []
            for n in range(30):
                filename_fun = f'population_size_adjustment/fun/FUN.POP_{population_size}-RUN_{n}'
                execution_solutions = read_solutions_objectives(filename_fun)
                execution_hypervolume = hypervolume.compute(execution_solutions)
                all_executions_values[key].append(execution_hypervolume / pareto_hypervolume)
            # print("KS: ",kstest(all_executions_values[key], "norm"))
    print(rank_test(all_executions_values))

if __name__ == "__main__":
    mutcross_adjustment()
    population_adjustment()

