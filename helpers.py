import copy
from jmetal.util.solution import (
    read_solutions,
    print_function_values_to_file,
    print_variables_to_file,
)

def dfs(visited, graph, node):
    if node not in visited:
        visited += [node]
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

def positive_correction(solution):
    res = copy.deepcopy(solution)
    for index, node in enumerate(solution.variables):
        for neighbor in node:
            if index not in [nbh for nbh in solution.variables[neighbor]]:
                res.variables[neighbor] += [index]
    return res

def negative_correction(solution):
    res = copy.deepcopy(solution)
    for index, node in enumerate(solution.variables):
        for neighbor in node:
            if index not in [nbh for nbh in solution.variables[neighbor]]:
                res.variables[index].remove(neighbor)
    return res


def get_border_solutions_pareto(pareto_file='evaluation/reference_pareto/FUN.PARETO_DFOM_SPEA2-NEIGHBORHOODS_GRAPH_CENTRAL_40'):
    pareto_front = read_solutions(pareto_file)
    min_cost = [10000000000, 0]
    max_conn = [0, 0]
    for solution in pareto_front:
        if solution.objectives[0] > 0 and solution.objectives[0] < min_cost[0]:
            min_cost = solution.objectives
        if solution.objectives[1] < max_conn[1]:
            max_conn = solution.objectives
    return (min_cost, max_conn)