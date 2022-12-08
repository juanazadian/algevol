from utils import NEIGHBORHOODS_GRAPH, NEIGHBORHOODS_INFORMATION

CENTRAL_INDEX = 40

def sum_solution_connectivity(solution):
    sum = 0
    for node in solution:
        sum += [nbh[2] for nbh in NEIGHBORHOODS_INFORMATION if nbh[0] == node][0]
    return sum


def mod_dfs(visited, graph, node, criterium, cost):
    if node not in visited:
        visited += [node]
        neighbours = graph[node]
        to_evaluate = [nbh for nbh in neighbours if nbh[0] not in visited]
        if len(to_evaluate) == 0:
            return
        neighbour = criterium(to_evaluate)
        cost[0] += [nbh[1] for nbh in neighbours if nbh[0] == neighbour][0]
        mod_dfs(visited, graph, neighbour, criterium, cost)

def min_distance(neighbours):
    minimun = min(neighbours, key=lambda tup: tup[1])
    return minimun[0]

def max_connectivity(neighbours):
    indexes = [nbh[0] for nbh in neighbours]
    populations = [nbh for nbh in NEIGHBORHOODS_INFORMATION if nbh[0] in indexes]
    maximum = max(populations, key=lambda tup: tup[2])
    return maximum[0]

if __name__ == "__main__":
    min_cost_greedy_solution = []
    solution_cost = [0]
    mod_dfs(min_cost_greedy_solution, NEIGHBORHOODS_GRAPH, CENTRAL_INDEX, min_distance, solution_cost)

    min_cost_greedy_values = [solution_cost[0], sum_solution_connectivity(min_cost_greedy_solution)]
    print(min_cost_greedy_values)

    max_conn_greedy_solution = []
    solution_cost = [0]
    mod_dfs(max_conn_greedy_solution, NEIGHBORHOODS_GRAPH, CENTRAL_INDEX, max_connectivity, solution_cost)
    max_conn_greedy_values = [solution_cost[0], sum_solution_connectivity(max_conn_greedy_solution)]
    print(max_conn_greedy_values)
