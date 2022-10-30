#!/bin/env python

from jmetal.algorithm.multiobjective.spea2 import SPEA2
from jmetal.operator import PolynomialMutation, SBXCrossover
from jmetal.problem import DTLZ2
from jmetal.util.solution import (
    print_function_values_to_file,
    print_variables_to_file,
    read_solutions,
)
from jmetal.util.termination_criterion import StoppingByEvaluations

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

from dfom import DFOM
from mutation import GraphMutation
from crossover import GraphCrossover

if __name__ == "__main__":
    problem = DFOM()
    problem.reference_front = read_solutions(filename="resources/reference_front/DTLZ2.3D.pf")

    max_evaluations = 20000
    algorithm = SPEA2(
        problem=problem,
        population_size=20,
        offspring_population_size=20,
        mutation=GraphMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
        crossover=GraphCrossover(probability=0.5), # That probability can change.
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
    )

    algorithm.run()
    solutions = algorithm.get_result()

    print(f"Algorithm: {algorithm.get_name()}")
    print(f"Problem: {problem.get_name()}")
    print(f"Computing time: {algorithm.total_computing_time}")

    front = get_non_dominated_solutions(solutions)

    plot_front = Plot(plot_title='Pareto front approximation', axis_labels=['x', 'y'])
    plot_front.plot(front, label='SPEA2-ZDT1')
