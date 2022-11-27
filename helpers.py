import copy

def dfs(visited, graph, node):
    if node not in visited:
        visited += [node]
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

def positive_correction(solution):
    for index, node in enumerate(solution.variables):
        for neighbor in node:
            if index not in [nbh for nbh in solution.variables[neighbor]]:
                solution.variables[neighbor] += [index]

def negative_correction(solution):
    copi = copy.deepcopy(solution)
    for index, node in enumerate(solution.variables):
        for neighbor in node:
            if index not in [nbh for nbh in copi.variables[neighbor]]:
                solution.variables[index].remove(neighbor)

    def negative_correction(self, solution):
        copi = copy.deepcopy(solution)
        for index, node in enumerate(solution):
            for neighbor in node:
                if index not in [nbh for nbh in solution[neighbor]]:
                    print("corrige")
                    copi[index].remove(neighbor)
        return copi
