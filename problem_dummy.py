from jmetal.core.problem import Problem
from solution import GraphSolution
from abc import ABC
import random

def dfs(visited, graph, node):
    if node not in visited:
        visited += [node]
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

class DFOM(Problem[GraphSolution], ABC): # DFOM: Distribucion Fibra Optica Montevideo

    def __init__(self, number_of_variables: int = 6, number_of_objectives = 2):
        """ :param number_of_variables: number of decision variables of the problem.
        """
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.number_of_constraints = 0
        # self.obj_directions = [self.MINIMIZE] * number_of_objectives # Esto nose si está bien.
        # self.obj_labels = ['$ f_{} $'.format(i) for i in range(number_of_objectives)]
        self.barrios_montevideo = [ (0, "Central", 0), (1,"Pocitos", 110000), (2, "La Blanqueada", 80000),
        (3, "Tres Cruces", 20000), (4, "Punta Carretas", 40000), (5 , "Centro", 130000)] # Para tener un mapeo entre el indice y el nombre del barrio.
        self.grafo_barrios_montevideo = [ [(1, 6), (2, 1), (3, 5)], [(0, 6), (2, 5), (4, 3)],
        [(0, 1), (1, 5), (4, 6), (5, 4), (3, 5)], [(0, 5), (2, 5), (5, 2)],
        [(1, 3), (2, 6), (4, 6)], [(4, 6), (2, 4), (3, 2)] ] # Lista de adyacencia. Hay que definir bien los barrios y sus adyacentes. Va a ser una lista de listas de (barrio, costo).

    # --------  Solution corrections methods ----------

    def __positive_correction(self, solution):
        for index, node in enumerate(solution.variables):
            for neighbor in node:
                if index not in [nbh for nbh in solution.variables[neighbor]]:
                    solution.variables[neighbor] += [index]

    def __negative_correction(self, solution):
        for index, node in enumerate(solution.variables):
            for neighbor in node:
                if index not in [nbh for nbh in solution.variables[neighbor]]:
                    solution.variables[index].remove(neighbor)

    # --------  Centric solutions initialization methods ----------

    def __recursive_generate_centric_solution(self, solution, N, focused_nbh, visited_nbh):
        if N == 0:
            return
        else:
            for index in focused_nbh:
                nbh_neighbors = [nbh[0] for nbh in self.grafo_barrios_montevideo[index] ]

                # remove visited_nbh from random_neighbors
                not_visited_neighbors = [nbh for nbh in nbh_neighbors if nbh not in visited_nbh]

                # take N random neighbors from nbh_neighbors
                if N < len(not_visited_neighbors):
                    random_neighbors = random.sample(not_visited_neighbors, N)
                else:
                    random_neighbors = not_visited_neighbors

                visited_nbh += random_neighbors
                solution.variables[index] += random_neighbors

                self.__recursive_generate_centric_solution(solution, N-1, random_neighbors, visited_nbh)

    def __centric_solution_init_method(self, solution: GraphSolution):
        # Este metodo inicializa la solucion con barrios centricos.
        N=4
        self.__recursive_generate_centric_solution(solution, N, [0], [])

    # --------  Deep solutions initialization methods ----------

    def __recursive_generate_deep_solution(self, solution, N, focused_nbh, visited_nbh):
        if N == 0:
            return
        else:
            for index in focused_nbh:
                nbh_neighbors = [nbh[0] for nbh in self.grafo_barrios_montevideo[index]]

                # remove visited_nbh from random_neighbors
                not_visited_neighbors = [nbh for nbh in nbh_neighbors if nbh not in visited_nbh]

                picked_neighbor = random.sample(not_visited_neighbors, 1)

                visited_nbh += picked_neighbor
                solution.variables[index] += picked_neighbor

                self.__recursive_generate_deep_solution(solution, N-1, picked_neighbor, visited_nbh)

    def __deep_solutions_init_method(self, solution: GraphSolution):
        # Este metodo inicializa la solucion con grafos extensos.
        N = round(len(self.grafo_barrios_montevideo) / 2)
        self.__recursive_generate_deep_solution(solution, N, [0], [])

    # ---------------------------------------------------------------

    def create_solution(self) -> GraphSolution:
        new_solution = GraphSolution(
            self.number_of_variables,
            self.number_of_objectives,
            self.number_of_constraints)

        rand = random.random()

        if rand <= 0.5: # Corrijo quitando a la lista de adyacencia.
            self.__centric_solution_init_method(new_solution)
        else: # Corrijo agregando a la lista de adyacencia.
            self.__deep_solutions_init_method(new_solution)

        self.__positive_correction(new_solution)

        return new_solution

    # --------  Evaluation methods ----------

    def __sum_solution_costs(self, solution):
        sum = 0
        for index, node in enumerate(solution.variables):
            for connected_neighbor in node:
                for neighbor in self.grafo_barrios_montevideo[index]:
                    if neighbor[0] == connected_neighbor:
                        sum += neighbor[1]
        return sum/2

    def __sum_solution_connectivity(self, solution):
        sum = 0
        connected_nodes = []
        dfs(connected_nodes, solution.variables, 0)
        for node in connected_nodes:
            sum += [nbh[2] for nbh in self.barrios_montevideo if nbh[0] == node][0]
        return sum

    def evaluate(self, solution: GraphSolution) -> GraphSolution:
        solution.objectives = [0, 0]

        # Evaluo respecto a la funcion de costos
        solution.objectives[0] = self.__sum_solution_costs(solution)

        # Evaluo respecto a la función de conectividad
        solution.objectives[1] = self.__sum_solution_connectivity(solution)

        return solution

    def get_name(self):
        return 'DFOM'
