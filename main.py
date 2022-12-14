#!/bin/env python

from jmetal.algorithm.multiobjective.spea2 import SPEA2

from jmetal.util.termination_criterion import StoppingByEvaluations

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

from problem import DFOM
from mutation import GraphMutation
from crossover import GraphCrossover
from jmetal.lab.visualization import Plot
import matplotlib.pyplot as plt
from utils import NEIGHBORHOODS_GRAPH, NEIGHBORHOODS_INFORMATION, REDUCED_NEIGHBORHOODS_GRAPH, LAST_31_GRAPH
from helpers import make_graph

CENTRAL_INDEX = 40

if __name__ == "__main__":

    problem = DFOM(
        neighborhoods_information=NEIGHBORHOODS_INFORMATION,
        neighborhoods_graph=NEIGHBORHOODS_GRAPH,
        central_index=CENTRAL_INDEX,
    )

    max_evaluations = 20000
    algorithm = SPEA2(
        problem=problem,
        population_size=40,
        offspring_population_size=40,
        mutation=GraphMutation(probability=0.001, neighborhoods_graph = problem.neighborhoods_graph, distribution_index=20),
        crossover=GraphCrossover(probability=1), # Se puede ajustar esa probabilidad.
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
    )

    algorithm.run()
    solutions = algorithm.get_result()

    print(f"Algorithm: {algorithm.get_name()}")
    print(f"Problem: {problem.get_name()}")
    print(f"Solutions: {solutions}")
    print(f"Computing time: {algorithm.total_computing_time}")

    front = get_non_dominated_solutions(solutions)

    df = Plot.get_points(front)[0].rename(columns={0: "x", 1: "y"})
    df.plot(x = 'x', y = 'y', kind = "scatter", grid = True, legend = True, xlabel = 'cost', ylabel = 'connectivity')

    plt.show()
    # make_graph(front[0])
    # make_graph(front[9])
    # make_graph(front[19])




