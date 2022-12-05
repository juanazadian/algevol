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

def run_problem(mutation_probability, crossover_probability, population_size, graph = REDUCED_NEIGHBORHOODS_GRAPH, central_index = 0):
    problem = DFOM(
        neighborhoods_information=NEIGHBORHOODS_INFORMATION,
        neighborhoods_graph=graph,
        central_index=central_index,
    )
    max_evaluations = 20000
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
    return algorithm.get_result()


if __name__ == "__main__":

    mutation_probabilities = [0.001, 0.01, 0.1]
    crossover_probabilities = [0.5, 0.75, 1]
    population_sizes = [50, 125, 200]
    solutions = []
    for mutation_probability in mutation_probabilities:
        for crossover_probability in crossover_probabilities:
            for population_size in population_sizes:
                for n in range(30):
                    solutions += run_problem(mutation_probability, crossover_probability, population_size)
    reference_pareto_front = get_non_dominated_solutions(solutions)
    print_function_values_to_file(reference_pareto_front, "FUN." + 'DFOM_SPEA2')
    print_variables_to_file(reference_pareto_front, "VAR." + 'DFOM_SPEA2')
