import random

from jmetal.core.operator import Mutation
from solution import GraphSolution
from jmetal.util.ckecking import Check

class GraphMutation(Mutation[GraphSolution]):

    def __init__(self, probability: float, neighborhoods_graph: list, distribution_index: float = 0.20):
        super(GraphMutation, self).__init__(probability=probability)
        self.neighborhoods_graph = neighborhoods_graph
        self.distribution_index = distribution_index # No se si se va a usar esto, pero lo dejo por las dudas. Creo q con probability ya esta.

    def execute(self, solution: GraphSolution) -> GraphSolution:
        Check.that(issubclass(type(solution), GraphSolution), "Solution type invalid")

        # random number between 1 and number_of_variables
        random_index = random.randint(0, solution.number_of_variables - 1) # No se está considerando la central. Podría considerarse tambien.
        # TODO: podriamos ver de excluir la central de la mutacion
        possible_neighbors = self.neighborhoods_graph[random_index]

        picked_neighbor = random.sample(possible_neighbors, 1)[0][0]

        if picked_neighbor in solution.variables[random_index]:
            solution.variables[random_index].remove(picked_neighbor)
            solution.variables[picked_neighbor].remove(random_index)
        else:
            solution.variables[random_index] += [picked_neighbor]
            solution.variables[picked_neighbor] += [random_index]

        return solution

    def get_name(self):
        return 'Graph mutation'
