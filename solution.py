from jmetal.core.solution import Solution

class GraphSolution(Solution):
    """ Class representing Graph solutions """

    def __init__(self, number_of_variables: int, number_of_objectives: int, number_of_constraints: int = 0):
        super(GraphSolution, self).__init__(number_of_variables, number_of_objectives, number_of_constraints)

    def __copy__(self):
        new_solution = GraphSolution(
            self.number_of_variables,
            self.number_of_objectives)
        new_solution.objectives = self.objectives[:]
        new_solution.variables = self.variables[:]

        new_solution.attributes = self.attributes.copy()

        return new_solution
