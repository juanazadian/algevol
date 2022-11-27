from jmetal.core.solution import Solution
from typing import List


GraphType = List[int]
class GraphSolution(Solution[GraphType]):
    """ Class representing Graph solutions """

# Number of variables, va a ser la cantidad de barrios de Montevideo. Y cada una de esas variables va a ser una lista de enteros.
# Osea, los barrios adyacentes.
    def __init__(self, number_of_variables: int = 62, number_of_objectives: int = 2, number_of_constraints: int = 0):
        super(GraphSolution, self).__init__(number_of_variables, number_of_objectives, number_of_constraints)

    def __copy__(self):
        new_solution = GraphSolution(
            self.number_of_variables,
            self.number_of_objectives)
        new_solution.objectives = self.objectives[:]
        new_solution.variables = self.variables[:]

        new_solution.attributes = self.attributes.copy()

        return new_solution
