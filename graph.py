import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


# Define a helper function that returns a random subset of unique elements from lst with the specified size
def _random_subset(lst, size):
    if size >= len(lst):
        return lst
    else:
        return random.sample(lst, size)

# Define a function that generates a Barabasi-Albert random graph with n nodes and m initial edges per node


def barabasi_albert_graph(n, m, seed=None):
    # Set the random seed for reproducibility
    if seed is not None:
        random.seed(seed)

    # Create an empty graph with m nodes
    G = nx.empty_graph(m)
    targets = list(range(m))
    repeated_nodes = []
    source = m

    while source < n:
        # Add edges to the new node from m existing nodes
        G.add_edges_from(zip([source]*m, targets))

        # Update the list of repeated nodes proportional to their degree
        repeated_nodes.extend(targets)
        repeated_nodes.extend([source]*m)

        # Choose m unique nodes from the repeated nodes using preferential attachment
        targets = _random_subset(repeated_nodes, m)

        # Move to the next node
        source += 1

    return G

# Define a function that finds the shortest path between two nodes in a graph using Breadth-First Search (BFS)


def bfs_shortest_path(adjacency_dict, start_node, end_node):
    # If either the start or end node is not in the adjacency dictionary, return None
    if start_node not in adjacency_dict or end_node not in adjacency_dict:
        return None

    # Initialize the visited set and the queue with the start node and an empty path
    visited = set()
    queue = deque([(start_node, [])])

    while queue:
        # Pop the first node and its path from the queue
        node, path = queue.popleft()

        # If the node is the end node, return the path
        if node == end_node:
            return path + [node]

        # If the node has already been visited, skip it
        if node in visited:
            continue

        # Add the node to the visited set
        visited.add(node)

        # Add the node's neighbors to the queue with the current path appended
        for neighbor in adjacency_dict[node]:
            queue.append((neighbor, path + [node]))

    # If the end node is not reachable from the start node, return None
    return None

# Define a function that simulates sending a fixed amount of currency from one node to another in the graph


def send_amount(adj_list):
    amount = 1
    # Choose two random nodes in the graph
    node1 = random.randint(0, 99)
    node2 = random.randint(0, 99)
    while node2 == node1:
        node2 = random.randint(0, 99)

    # Find the shortest path between the two nodes using BFS
    path = bfs_shortest_path(adj_list, node1, node2)

    # If there is no path between the two nodes, keep trying until there is
    while (path == None):
        path = bfs_shortest_path(adj_list, node1, node2)

    return amount, path

# Define a function that plots the number of valid transactions against the total number of transactions


def plot_graph(y_list):
    x_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # plot the data
    plt.plot(x_list, y_list)
    fig, ax = plt.subplots()

    # plot the data
    ax.plot(x_list, y_list)
    ax.set_title('Transaction Status')
    # set the labels for x and y axis
    ax.set_xlabel('Total Transactions')
    ax.set_ylabel('Valid Transactions')

    # save the plot as an image
    plt.savefig('TxStatus.png')


# if __name__ == '__main__':
#     # Generate a Barabasi-Albert random graph with 40 nodes and 2 initial edges per node
#     G = barabasi_albert_graph(100, 2)

#     # Get the adjacency list of the graph
#     adj_list = nx.to_dict_of_lists(G)
#     print(adj_list)
#     for i in range(100):
#         node1,node2,amount,path = send_amount(adj_list)
#         print(node1,node2,path)
#     nx.draw(G, with_labels=True)
#     plt.show()
