import random

from jmetal.core.operator import Mutation
from solution import GraphSolution
from jmetal.util.ckecking import Check

class GraphMutation(Mutation[GraphSolution]):

    def __init__(self, probability: float, distribution_index: float = 0.20):
        super(GraphMutation, self).__init__(probability=probability)
        self.distribution_index = distribution_index # No se si se va a usar esto, pero lo dejo por las dudas. Creo q con probability ya esta.

    def execute(self, solution: GraphSolution) -> GraphSolution:
        Check.that(issubclass(type(solution), GraphSolution), "Solution type invalid")

        # modifico "sulution" con la mutacion que dijimos, y la devuelvo.
        return solution

    def get_name(self):
        return 'Graph mutation'