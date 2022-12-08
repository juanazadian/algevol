#!/bin/env python

from jmetal.algorithm.multiobjective.spea2 import SPEA2
from jmetal.algorithm.multiobjective.nsgaii import NSGAII

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
from utils import *
from jmetal.util.solution import (
    print_function_values_to_file,
    print_variables_to_file,
)

import multiprocessing as mp

results = []

def run_spea(mutation_probability, crossover_probability, population_size, run, graph = NEIGHBORHOODS_GRAPH, central_index = 40):
    problem = DFOM(
        neighborhoods_information=NEIGHBORHOODS_INFORMATION,
        neighborhoods_graph=graph,
        central_index=central_index,
    )

    max_evaluations = 25000

    experiment = SPEA2(
        problem=problem,
        population_size=population_size,
        offspring_population_size=population_size,
        mutation=GraphMutation(probability=mutation_probability, neighborhoods_graph = problem.neighborhoods_graph, distribution_index=20),
        crossover=GraphCrossover(probability=crossover_probability),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
    )

    experiment.run()
    print(f"Algorithm: {experiment.get_name()}")
    print(f"Computing time: {experiment.total_computing_time}")
    solutions = experiment.get_result()
    print_function_values_to_file(solutions, f'evaluation/fun/FUN.{experiment.get_name()}-RUN_{run}')
    print_variables_to_file(solutions, f'evaluation/var/VAR.{experiment.get_name()}-RUN_{run}')

    return solutions

def run_nsga(mutation_probability, crossover_probability, population_size, run, graph = NEIGHBORHOODS_GRAPH, central_index = 40):
    problem = DFOM(
        neighborhoods_information=NEIGHBORHOODS_INFORMATION,
        neighborhoods_graph=graph,
        central_index=central_index,
    )

    max_evaluations = 25000

    experiment = NSGAII(
        problem=problem,
        population_size=population_size,
        offspring_population_size=population_size,
        mutation=GraphMutation(probability=mutation_probability, neighborhoods_graph = problem.neighborhoods_graph, distribution_index=20),
        crossover=GraphCrossover(probability=crossover_probability),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
    )

    experiment.run()
    print(f"Algorithm: {experiment.get_name()}")
    print(f"Computing time: {experiment.total_computing_time}")
    solutions = experiment.get_result()
    print_function_values_to_file(solutions, f'evaluation/fun/FUN.{experiment.get_name()}-RUN_{run}')
    print_variables_to_file(solutions, f'evaluation/var/VAR.{experiment.get_name()}-RUN_{run}')

    return solutions

def collect_result(result):
    global results
    results.append(result)

if __name__ == "__main__":
    pool = mp.Pool(mp.cpu_count())

    solutions = []

    instances = [(NEIGHBORHOODS_GRAPH, 40), (FIRST_31_GRAPH, 15), (LAST_31_GRAPH, 15), (FIRST_31_GRAPH, 25), (LAST_31_GRAPH, 25)]
    for instance in instances:
        graph = instance[0]
        central_location = instance[1]
        for n in range(30):
            pool.apply_async(run_spea, args=(0.001, 1.0, 40, n, graph, central_location), callback = collect_result)
            pool.apply_async(run_nsga, args=(0.001, 1.0, 40, n, graph, central_location), callback = collect_result)

    pool.close()
    pool.join()

    flat_list = [item for sublist in results for item in sublist]

    reference_pareto_front = get_non_dominated_solutions(flat_list)
    print("pareto: ", reference_pareto_front)
    print_function_values_to_file(reference_pareto_front, "evaluation/FUN." + 'PARETO_DFOM_SPEA2')
    print_variables_to_file(reference_pareto_front, "evaluation/VAR." + 'PARETO_DFOM_SPEA2')
