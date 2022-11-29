import random
import copy

def dfs(visited, graph, node):
    if node not in visited:
        visited += [node]
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

class TEST:

    def __init__(self):
        self.neighborhoods_population = [ (0, "Central", 0), (1,"Pocitos", 110000), (2, "La Blanqueada", 80000),
        (3, "Tres Cruces", 20000), (4, "Punta Carretas", 40000), (5 , "Centro", 130000)]
        self.neighborhoods_graph = [ [(1, 6), (2, 1), (3, 5)], [(0, 6), (2, 5), (4, 3)],
        [(0, 1), (1, 5), (4, 6), (5, 4), (3, 5)], [(0, 5), (2, 5), (5, 2)],
        [(1, 3), (2, 6), (4, 6)], [(4, 6), (2, 4), (3, 2)] ]


    def sum_solution_costs(self, solution):
        sum = 0
        for index, node in enumerate(solution):
            for neighbor in node:
                sum += [nbh[1] for nbh in self.neighborhoods_graph[index] if nbh[0] == neighbor][0]
        return sum/2

    def sum_solution_connectivity(self, solution):
        sum = 0
        connected_nodes = []
        dfs(connected_nodes, solution, 0)
        for node in connected_nodes:
            sum += [nbh[2] for nbh in self.neighborhoods_population if nbh[0] == node][0]
        return sum

    def positive_correction(self, solution):
        for index, node in enumerate(solution):
            for neighbor in node:
                if index not in [nbh for nbh in solution[neighbor]]:
                    solution[neighbor] += [index]


    def negative_correction(self, solution):
        copi = copy.deepcopy(solution)
        for index, node in enumerate(solution):
            for neighbor in node:
                if index not in [nbh for nbh in solution[neighbor]]:
                    print("corrige")
                    copi[index].remove(neighbor)
        return copi


    def __recursive_generate_solution(self, solution, N, focused_nbh, visited_nbh):
        if N == 0:
            return
        else:
            for index in focused_nbh:
                nbh_neighbors = [nbh[0] for nbh in self.neighborhoods_graph[index] ]

                # remove visited_nbh from random_neighbors
                not_visited_neighbors = [nbh for nbh in nbh_neighbors if nbh not in visited_nbh]

                # take N random neighbors from nbh_neighbors
                if N < len(not_visited_neighbors):
                    random_neighbors = random.sample(not_visited_neighbors, N)
                else:
                    random_neighbors = not_visited_neighbors

                visited_nbh += random_neighbors
                solution[index] += random_neighbors

                self.__recursive_generate_solution(solution, N-1, random_neighbors, visited_nbh)

    def centric_solutions_init_method(self, solution):
        # Este metodo inicializa la solucion con grafos centricos.
        N=2
        self.__recursive_generate_solution(solution, N, [0], [])

    def __recursive_generate_deep_solution(self, solution, N, focused_nbh, visited_nbh):
        if N == 0:
            return
        else:
            for index in focused_nbh:
                nbh_neighbors = [nbh[0] for nbh in self.neighborhoods_graph[index]]

                # remove visited_nbh from random_neighbors
                not_visited_neighbors = [nbh for nbh in nbh_neighbors if nbh not in visited_nbh]

                picked_neighbor = random.sample(not_visited_neighbors, 1)

                visited_nbh += picked_neighbor
                solution[index] += picked_neighbor

                self.__recursive_generate_solution(solution, N-1, picked_neighbor, visited_nbh)

    def deep_solutions_init_method(self, solution):
        # Este metodo inicializa la solucion con grafos extensos.
        N = round(len(self.neighborhoods_graph) / 2)
        self.__recursive_generate_deep_solution(solution, N, [0], [])

def test_centric_solutions(test, solution):
    test.centric_solutions_init_method(solution)
    print("CEntric Solucion no corregida", solution)
    test.negative_correction(solution)
    print("Centric Solucion corregida",solution)
    print(test.sum_solution_connectivity(solution))
    # print(test.sum_solution_costs(solution))

def test_deep_solutions(test, solution):
    test.deep_solutions_init_method(solution)
    print("DEep Solucion no corregida", solution)
    res = test.negative_correction(solution)
    print("Deep Solucion corregida",res)
    print(test.sum_solution_costs(solution))

if __name__ == "__main__":
    solution = [[] for _ in range(6)]
    test = TEST()
    test_deep_solutions(test, solution)
    # solution = [[] for _ in range(6)]
    # test_deep_solutions(test, solution)

