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
        picked_nbh = random.randint(1, solution.number_of_variables - 1) # No se está considerando la central. Podría considerarse tambien.

        possible_neighbors = self.neighborhoods_graph[picked_nbh]

        picked_neighbor = random.sample(possible_neighbors, 1)[0][0]

        if picked_neighbor in solution.variables[picked_nbh]:
            solution.variables[picked_nbh].remove(picked_neighbor)
            solution.variables[picked_neighbor].remove(picked_nbh)
        else:
            solution.variables[picked_nbh] += [picked_neighbor]
            solution.variables[picked_neighbor] += [picked_nbh]

        return solution

    def get_name(self):
        return 'Graph mutation'
