from pathlib import Path
import ast
from solution import GraphSolution
from jmetal.util.solution import read_solutions

""" Reads a reference front from a file.

:param filename: File path where the front is located.
"""
front = []

def read_solutions_variables(filename_var):
    solutions = []
    with open(filename_var) as file:
        for line in file:
            line = line.replace(' [', '#[').replace(' \n', '').split('#')
            array = [ast.literal_eval(li) for li in line]
            solution = GraphSolution(number_of_variables=len(array), number_of_objectives = 2)
            solution.variables = array
            solutions.append(solution)
    return solutions

def read_solutions_objectives(filename: str):
    objective_values = []
    with open(filename) as file:
        for line in file:
            vector = [float(x) for x in line.split()]
            objective_values.append(vector)
    return objective_values

if __name__ == "__main__":
    # print(read_solutions_variables("VAR.PARETO_DFOM_SPEA2"))
    print(read_solutions_objectives("FUN.PARETO_DFOM_SPEA2"))
