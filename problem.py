from jmetal.core.problem import Problem
from solution import GraphSolution
from abc import ABC
import random

class DFOM(Problem[GraphSolution], ABC): # DFOM: Distribucion Fibra Optica Montevideo

    def __init__(self, number_of_variables: int = 62, number_of_objectives=2):
        """ :param number_of_variables: number of decision variables of the problem.
        """
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        # self.number_of_constraints = 0
        # self.obj_directions = [self.MINIMIZE] * number_of_objectives # Esto nose si está bien.
        # self.obj_labels = ['$ f_{} $'.format(i) for i in range(number_of_objectives)] 
        self.barrios_montevideo = [i for i in range(1, 63)] # Para tener un mapeo entre el indice y el nombre del barrio.
        self.grafo_barrios_montevideo = [] # Lista de adyacencia. Hay que definir bien los barrios y sus adyacentes. Va a ser una lista de listas de (barrio, costo).

    def recursive_generate_solution(self, solution: GraphSolution, N, focused_nbh, visited_nbh):
        if N == 0:
            return
        else:
            for nbh in focused_nbh:
                nbh_neighbors = self.grafo_barrios_montevideo[nbh]
                # take N random neighbors from nbh_neighbors
                random_neighbors = random.sample(nbh_neighbors, N)
                # remove visited_nbh from random_neighbors
                random_neighbors_not_visited = [nbh for nbh in random_neighbors if nbh not in visited_nbh]

                visited_nbh += random_neighbors_not_visited
                solution.variables[nbh] += random_neighbors_not_visited
                self.recursive_generate_solution(solution, N-1, random_neighbors)
            

    def centric_solutions_init_method(self, solution: GraphSolution):
        # Este metodo inicializa la solucion con barrios centricos.
        N=4
        self.recursive_generate_solution(solution, N, [0])
        

    def create_solution(self) -> GraphSolution:
        new_solution = GraphSolution(
            self.number_of_variables,
            self.number_of_objectives,
            self.number_of_constraints)

        rand = random.random()

        if rand <= 0.5: # Corrijo quitando a la lista de adyacencia.
            self.centric_solutions_init_method(new_solution)
        else: # Corrijo agregando a la lista de adyacencia.
            deep_solutions_init_method(new_solution)

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
