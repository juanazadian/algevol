from pathlib import Path
from jmetal.core.quality_indicator import *
import ast
from solution import GraphSolution
from solution_parser import read_solutions_objectives, read_solutions_variables

""" Reads a reference front from a file.

:param filename: File path where the front is located.
"""

if __name__ == "__main__":
    mutation_probabilities = [0.001, 0.01, 0.1]
    crossover_probabilities = [0.5, 0.75, 1]
    all_executions_values = {}
    reference_pareto = read_solutions_objectives('reference/FUN.PARETO_DFOM_SPEA2')
    hypervolume = HyperVolume([45000, 0])
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
    print(all_executions_values)

