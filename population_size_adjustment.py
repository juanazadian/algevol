#!/bin/env python

from jmetal.algorithm.multiobjective.spea2 import SPEA2

from jmetal.util.termination_criterion import StoppingByEvaluations

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

from problem import DFOM
from mutation import GraphMutation
from crossover import GraphCrossover
from jmetal.lab.visualization import Plot
from pandas import DataFrame
import matplotlib.pyplot as plt
import networkx as nx
from utils import NEIGHBORHOODS_INFORMATION, REDUCED_NEIGHBORHOODS_GRAPH
from jmetal.util.solution import (
    print_function_values_to_file,
    print_variables_to_file,
)

import multiprocessing as mp

results = []

def run_problem(mutation_probability, crossover_probability, population_size, run, graph = REDUCED_NEIGHBORHOODS_GRAPH, central_index = 10):
    problem = DFOM(
        neighborhoods_information=NEIGHBORHOODS_INFORMATION,
        neighborhoods_graph=graph,
        central_index=central_index,
    )
    max_evaluations = 25000
    algorithm = SPEA2(
        problem=problem,
        population_size=population_size,
        offspring_population_size=population_size,
        mutation=GraphMutation(probability=mutation_probability, neighborhoods_graph = problem.neighborhoods_graph, distribution_index=20),
        crossover=GraphCrossover(probability=crossover_probability),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
    )
    algorithm.run()
    print(f"Algorithm: {algorithm.get_name()}")
    print(f"Problem: {problem.get_name()}")
    print(f"Computing time: {algorithm.total_computing_time}")
    solutions = algorithm.get_result()
    print_function_values_to_file(solutions, f'population_size_adjustment/fun/FUN.POP_{population_size}-RUN_{run}')
    print_variables_to_file(solutions, f'population_size_adjustment/var/VAR.POP_{population_size}-RUN_{run}')

    return solutions

def collect_result(result):
    global results
    results.append(result)

if __name__ == "__main__":
    population_sizes = [20, 40, 60]
    pool = mp.Pool(mp.cpu_count())

    solutions = []
    for population_size in population_sizes:
        for n in range(30):
            pool.apply_async(run_problem, args=(0.01, 1, population_size, n), callback = collect_result)

    pool.close()
    pool.join()

    flat_list = [item for sublist in results for item in sublist]

    reference_pareto_front = get_non_dominated_solutions(flat_list)
    print("pareto: ", reference_pareto_front)
    print_function_values_to_file(reference_pareto_front, "population_size_adjustment/reference/FUN." + 'PARETO_DFOM_SPEA2')
    print_variables_to_file(reference_pareto_front, "population_size_adjustment/reference/VAR." + 'PARETO_DFOM_SPEA2')
