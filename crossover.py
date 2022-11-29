from jmetal.core.operator import Crossover
from solution import GraphSolution
from typing import List
from jmetal.util.ckecking import Check
from helpers import *
import random
import copy


class GraphCrossover(Crossover[GraphSolution, GraphSolution]):

    def __init__(self, probability: float):
        super(GraphCrossover, self).__init__(probability=probability)
    # Esta probabilidad es la que me dice si corrijo postiva o negativamente (agregando a la lista de adyacencia o quitando de la lista de adyacencia)
    # la accedo como "self.probability"

    def execute(self, parents: List[GraphSolution]) -> List[GraphSolution]:
        # chequeo que el cruzamiento sea de 2 padres, y que el tipado sea el correcto
        Check.that(issubclass(type(parents[0]), GraphSolution), "Solution type invalid")
        Check.that(issubclass(type(parents[1]), GraphSolution), "Solution type invalid")
        Check.that(len(parents) == 2, 'The number of parents is not two: {}'.format(len(parents)))
        # Arranco con los hijos iguales a los nuevos padres en este caso. (pa inicializar en realidad, capaz no va esto)
        offspring = [copy.deepcopy(parents[0]), copy.deepcopy(parents[1])]

        N = len(offspring[0].variables)
        nbh_to_cross = random.sample(list(range(N)), round(N/3))

        for nbh in nbh_to_cross:
            to_cross = offspring[0].variables[nbh]
            offspring[0].variables[nbh] = offspring[1].variables[nbh]
            offspring[1].variables[nbh] = to_cross

        if random.random() <= 0.5:
            offspring_0 = positive_correction(offspring[0])
            offspring_1 =positive_correction(offspring[1])
        else:
            offspring_0 = negative_correction(offspring[0])
            offspring_1 = negative_correction(offspring[1])

        return [offspring_0, offspring_1]

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self) -> str:
        return 'Graph as adjacency list Crossover'
