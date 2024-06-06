import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from numpy import mean
from numpy.linalg import matrix_power


def matrix(rebra, orient):
    n = 0
    for i in rebra:
        n = max(n, i[0] + 1, i[1] + 1)
    matrica = np.zeros((n, n), dtype="float32")
    for line in rebra:
        if orient:
            matrica[line[0]][line[1]] = line[2]
        else:
            matrica[line[0]][line[1]] = line[2]
            matrica[line[1]][line[0]] = line[2]
    for i in range(n):
        k = sum(matrica[i])
        if k != 0:
            for j in range(n):
                matrica[i][j] /= k
    return matrica


def generate_random_graphs(num_graphs, directed=False):
    graph_list = []
    for _ in range(num_graphs):
        if directed:
            num_nodes = np.random.randint(3, 20)
            num_edges = num_nodes
            G = nx.gnp_random_graph(num_nodes, num_edges / num_nodes, directed=True)
            graph_list.append(G)
        else:
            num_nodes = np.random.randint(3, 20)
            num_edges = num_nodes * (num_nodes + 1) // 2
            G = nx.gnp_random_graph(num_nodes, num_edges / num_nodes, directed=False)
            graph_list.append(G)
    return graph_list


def get_random_input_data_for_graph(G):
    num_nodes = G.number_of_nodes()
    rebra = [[e[0], e[1], np.random.randint(1, 100)] for e in G.edges()]
    x0 = list(np.random.randint(100, size=num_nodes))
    return rebra, x0


def run_and_visualize_deGroot_for_graphs(graph_list, orient, num_iterations):
    fig, axs = plt.subplots(3, 3, figsize=(15, 15))
    fig.suptitle('DeGroot Dynamics for Graphs')

    for i in range(3):
        for j in range(3):
            G = graph_list[i * 3 + j]
            rebra, x0 = get_random_input_data_for_graph(G)
            #print('Тест',i*3+j+10)
            #print(1)
            #print(1)
            #for r in rebra:
            #    print(r[0] + 1, r[1]+1, r[2])
            #print(0)
            #print(*x0)
            #print(10)
            #print('---------------')
            w = matrix(rebra, orient)

            spisok_x = []
            for k in range(num_iterations):
                spisok_x.append(np.dot(matrix_power(w, k + 1), x0))
            sostoinia = np.array(spisok_x).transpose()
            x = range(num_iterations)
            for node_states in sostoinia:
                axs[i, j].plot(x, node_states)

    plt.show()
def generate_directed_graphs_without_cycles(n, num_nodes):
    graph_list = []
    for _ in range(n):
        G = nx.gnr_graph(num_nodes, 0.3, directed=True)
        while not nx.is_directed_acyclic_graph(G):
            G = nx.gnr_graph(num_nodes, 0.3, directed=True)
        graph_list.append(G)

    return graph_list

def generate_directed_graphs_with_cycles(n, num_nodes):
    graph_list = []
    for _ in range(n):
        G = nx.DiGraph()
        nodes = list(range(num_nodes))
        G.add_nodes_from(nodes)
        for i in range(num_nodes):
            possible_targets = [v for v in nodes if v != i]
            target = random.choice(possible_targets)
            G.add_edge(i, target)
        graph_list.append(G)

    return graph_list
def main():
    num_graphs = 9

    # Test case for 9 random undirected graphs
    #undirected_graph_list = generate_random_graphs(num_graphs, directed=False)
    #run_and_visualize_deGroot_for_graphs(undirected_graph_list, orient=False, num_iterations=10)

    # Test case for 9 random directed graphs with cycles
    directed_graph_list_with = generate_directed_graphs_with_cycles(num_graphs, 8)
    run_and_visualize_deGroot_for_graphs(directed_graph_list_with, orient=True, num_iterations=10)

    # Test case for 9 random directed graphs without cycles
    #directed_graph_list_without = generate_directed_graphs_without_cycles(num_graphs, 8)
    #run_and_visualize_deGroot_for_graphs(directed_graph_list_without, orient=True, num_iterations=1000)

if __name__ == "__main__":
    main()
