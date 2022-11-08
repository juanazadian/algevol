import random

barrios_montevideo = [ (0,"Central"), (1,"Pocitos"), (2,"La Blanqueada"),
(3,"Tres Cruces"), (4,"Punta Carretas"), (5,"Centro")]
grafo_barrios_montevideo = [ [(1, 6), (2, 1), (3, 5)], [(0, 6), (2, 5), (4, 3)], 
[(0, 1), (1, 5), (4, 6), (5, 4), (3, 5)], [(0, 5), (2, 5), (5, 2)],
 [(1, 3), (2, 6), (4, 6)], [(4, 6), (2, 4), (3, 2)] ]


def positive_correction(solution):
    for index, node in enumerate(solution):
        # print("Inside Loop", node, index)
        # nbh_neighbors_indexes = [nbh[0] for nbh in node]
        for neighbor, cost in node:
            if index not in [nbh[0] for nbh in solution[neighbor]]:
                # print("Inside if not", node,cost,solution[neighbor])

                solution[neighbor] += [(index, cost)]
        # print("Despues de iteracion:", index, "Solucion:", solution)
            

def recursive_generate_solution(solution, N, focused_nbh, visited_nbh):
    if N == 0:
        return
    else:
        for index, cost in focused_nbh:
            nbh_neighbors = grafo_barrios_montevideo[index]

            # remove visited_nbh from random_neighbors
            not_visited_neighbors = [nbh for nbh in nbh_neighbors if nbh[0] not in visited_nbh]

            # take N random neighbors from nbh_neighbors
            if N < len(not_visited_neighbors):
                random_neighbors = random.sample(not_visited_neighbors, N)
            else:
                random_neighbors = not_visited_neighbors
                 

            visited_nbh += [nbh[0] for nbh in random_neighbors]
            solution[index] += random_neighbors

            recursive_generate_solution(solution, N-1, random_neighbors, visited_nbh)

if __name__ == "__main__":
    solution = [[] for _ in range(6)]
    recursive_generate_solution(solution, 2, [(0, 0)], [])
    print("Solucion no corregida", solution)
    positive_correction(solution)
    print("Solucion corregida",solution)

