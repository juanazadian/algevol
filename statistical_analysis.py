from pathlib import Path
from jmetal.core.quality_indicator import *
import ast
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
    data = np.array(reference_pareto)
    return [data[:,0].max(), data[:,1].max()]

if __name__ == "__main__":
    mutation_probabilities = [0.001, 0.01, 0.1]
    crossover_probabilities = [0.5, 0.75, 1]
    all_executions_values = {}
    all_executions_statistics = {}
    reference_pareto = read_solutions_objectives('reference/FUN.PARETO_DFOM_SPEA2')
    hypervolume = HyperVolume(nadir(reference_pareto))
    pareto_hypervolume = hypervolume.compute(reference_pareto)

    for mutation_probability in mutation_probabilities:
        for crossover_probability in crossover_probabilities:
            key = f'MUT_{mutation_probability}-CROSS_{crossover_probability}'
            all_executions_values[key] = []
            all_executions_statistics[key] = []
            for n in range(30):
                filename_fun = f'data/fun/FUN.MUT_{mutation_probability}-CROSS_{crossover_probability}-RUN_{n}'
                execution_solutions = read_solutions_objectives(filename_fun)
                execution_hypervolume = hypervolume.compute(execution_solutions)
                all_executions_values[key].append(execution_hypervolume / pareto_hypervolume)
            all_executions_statistics[key].append(statistics(all_executions_values[key]))
            print("KS: ",kstest(all_executions_values[key], "norm"))
    print(all_executions_statistics)

