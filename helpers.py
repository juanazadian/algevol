import copy
from jmetal.util.solution import (
    read_solutions,
    print_function_values_to_file,
    print_variables_to_file,
)
import matplotlib.pyplot as plt
import networkx as nx
from solution_parser import read_solutions_variables

def make_graph(solution):
    G = nx.Graph()
    for index, node in enumerate(solution.variables):
        for nbh in node:
            G.add_edge(index, nbh)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

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


def get_border_solutions_pareto(
    pareto_fun_file='evaluation/reference_pareto/FUN.PARETO_DFOM_SPEA2-NEIGHBORHOODS_GRAPH_CENTRAL_40',
    pareto_var_file='evaluation/reference_pareto/VAR.PARETO_DFOM_SPEA2-NEIGHBORHOODS_GRAPH_CENTRAL_40',
):
    pareto_front = read_solutions(pareto_fun_file)
    min_cost = [10000000000, 0]
    min_cost_index = -1
    max_conn = [0, 0]
    max_conn_index = -1
    index_middle=round(len(pareto_front)/2)
    for index, solution in enumerate(pareto_front):
        if solution.objectives[0] > 0 and solution.objectives[0] < min_cost[0]:
            min_cost_index = index
            min_cost = solution.objectives
        if solution.objectives[1] < max_conn[1]:
            max_conn_index = index
            max_conn = solution.objectives
    solutions_var = read_solutions_variables(pareto_var_file)
    min_cost_vars = solutions_var[min_cost_index]
    max_conn_vars = solutions_var[max_conn_index]
    index_middle_vars = solutions_var[index_middle]
    make_graph(min_cost_vars)
    make_graph(max_conn_vars)
    make_graph(index_middle_vars)
    # print(min_cost_vars.variables)
    # print(max_conn_vars.variables)
    return (min_cost, max_conn)