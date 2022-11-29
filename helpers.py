import copy

def dfs(visited, graph, node):
    if node not in visited:
        visited += [node]
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

def positive_correction(solution):
    copi = copy.deepcopy(solution)
    for index, node in enumerate(solution.variables):
        for neighbor in node:
            if index not in [nbh for nbh in solution.variables[neighbor]]:
                copi.variables[neighbor] += [index]
    return copi

def negative_correction(solution):
    copi = copy.deepcopy(solution)
    for index, node in enumerate(solution.variables):
        for neighbor in node:
            if index not in [nbh for nbh in solution.variables[neighbor]]:
                copi.variables[index].remove(neighbor)
    return copi
