from jmetal.core.problem import Problem
from solution import GraphSolution
from abc import ABC
import random

# random list with numbers from 1 to 62
def random_list():
    return random.sample(range(1, 63), 62)

class DFOM(Problem[GraphSolution], ABC): # DFOM: Distribucion Fibra Optica Montevideo

    def __init__(self, number_of_variables: int = 62, number_of_objectives=2):
        """ :param number_of_variables: number of decision variables of the problem.
        """
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.number_of_constraints = 0
        self.obj_directions = [self.MINIMIZE] * number_of_objectives # Esto nose si está bien.
        self.obj_labels = ['$ f_{} $'.format(i) for i in range(number_of_objectives)] 
        self.barrios_montevideo = [i for i in range(1, 63)] # Esto es para que no se repitan los barrios en la lista de adyacencia.
        self.grafo_barrios_montevideo = [] # Lista de adyacencia. Hay que definir bien los barrios y sus adyacentes. Va a ser una lista de listas de (barrio, costo).

    def create_solution(self) -> GraphSolution:
        new_solution = GraphSolution(
            self.number_of_variables,
            self.number_of_objectives,
            self.number_of_constraints)
        new_solution.variables = \
            [random.sample(range(1, 63), 62) for i in 
             range(self.number_of_variables)]
             # Esto es inicializado totalmente random, y si todos los barrios estuvieran conectados entre si. Hay q cambiarlo por los 2
             # modelos que habiamos hablado en el informe. Cada variable (hay 62) es una lista de enteros, que son los barrios adyacentes a ese barrio.

        return new_solution

    def evaluate(self, solution: GraphSolution) -> GraphSolution:

        # Acá agarro self.grafo_barrios_montevideo y evaluo las funciones objetivo.

        # 

        k = self.number_of_variables - self.number_of_objectives + 1

        g = sum([(x - 0.5) * (x - 0.5) - cos(20.0 * pi * (x - 0.5))
                 for x in solution.variables[self.number_of_variables - k:]])

        g = 100 * (k + g)

        solution.objectives = [(1.0 + g) * 0.5] * self.number_of_objectives

        for i in range(self.number_of_objectives):
            for j in range(self.number_of_objectives - (i + 1)):
                solution.objectives[i] *= solution.variables[j]

            if i != 0:
                solution.objectives[i] *= 1 - solution.variables[self.number_of_objectives - (i + 1)]

        return solution

    def get_name(self):
        return 'DFOM'
