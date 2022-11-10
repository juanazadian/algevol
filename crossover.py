from jmetal.core.operator import Crossover
from solution import GraphSolution
from typing import List
from jmetal.util.ckecking import Check
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

        # Luego, Realizo el cruzamiento que pensamos.

        # Luego, debo corregir para que siga siendo una lista de adyacencia válida.
        rand = random.random()
        
        # if rand <= self.probability: # Corrijo quitando a la lista de adyacencia.
            # print("if")
        # else: # Corrijo agregando a la lista de adyacencia.
            # print("else")
        return offspring

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self) -> str:
        return 'Graph as adjacency list Crossover'