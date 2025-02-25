import building1
import networkx as nx
import matplotlib.pyplot as plt
import random

#data from building file
nodes = building1.nodes
edges = building1.edges
pheromones = building1.pheromones
heuristics = building1.heuristics
num_exits = building1.num_exits
#graph of building
building_graph = nx.DiGraph()
for edge in edges:
    building_graph.add_edge(edge[0], edge[1], **edge[2])

#parameters
num_ants = 10
num_iterations = 10
alpha = 0.5  #pheromone importance
beta = 0.5  #heuristic importance
evaporation_rate = 0.8
Q = 1  #pheromone constant


#fitness function
def fitness(path, graph):
    total_cost = 0
    for i in range(len(path) - 1):
        edge_data = graph[path[i]][path[i + 1]]
        total_cost += edge_data['distance'] + edge_data['risk']
    return total_cost


#probability of next step
def calculate_probabilities(current_node, unvisited_nodes, graph):
    probabilities = []
    denominator = 0

    #gets sum of total probability of all next steps as denomiator
    for neighbor in unvisited_nodes:
        if graph.has_edge(current_node, neighbor):
            pheromone = pheromones[(current_node, neighbor)]
            h = heuristics[(current_node, neighbor)]
            denominator += (pheromone ** alpha) * (h ** beta)
    #gets probability of a next possible step as nuemator
    for neighbor in unvisited_nodes:
        if graph.has_edge(current_node, neighbor):
            pheromone = pheromones[(current_node, neighbor)]
            h = heuristics[(current_node, neighbor)]
            numerator = (pheromone ** alpha) * (h ** beta)
            #all next nodes along with probabilites
            probabilities.append((neighbor, numerator / denominator))

    return probabilities


#simulate ants
def simulate_ants(graph, start_node, num_ants):
    paths = []
    path_lengths = []

    for _ in range(num_ants):
        current_node = start_node
        visited = [current_node]
        path_length = 0

        #gets list of next possible node
        while current_node not in [f"exit{i}" for i in range(1, num_exits + 1)]:
            unvisited_neighbors = [n for n in graph.neighbors(current_node) if n not in visited]

            #prevents infinite looping if ants are stuck
            if not unvisited_neighbors:
                break

            #randomly picks next node with weighting
            probabilities = calculate_probabilities(current_node, unvisited_neighbors, graph)
            next_node = random.choices(
                [p[0] for p in probabilities],
                weights=[p[1] for p in probabilities]
            )[0]
            edge_data = graph[current_node][next_node]
            #updates current path length
            path_length += edge_data['distance'] + edge_data['risk']
            visited.append(next_node)
            current_node = next_node

        #ends loop if exit is found
        if visited[-1] in [f"exit{i}" for i in range(1, num_exits + 1)]:  # Only count successful paths
            paths.append(visited)
            path_lengths.append(fitness(visited, graph))  # Use fitness function to calculate path length

    return paths, path_lengths


#pheromone update
def update_pheromones(paths, path_lengths):
    global pheromones
    #evaporate pheromones
    for edge in pheromones:
        pheromones[edge] *= (1 - evaporation_rate)

    #lay pheromones for successful paths
    for path, path_length in zip(paths, path_lengths):
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            pheromones[edge] += Q / path_length


#visualise path of ants
def visualize_graph(graph, pheromones, paths=[]):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
    edge_labels = {(u, v): f"D:{d['distance']} R:{d['risk']} P:{pheromones[(u, v)]:.2f}"
                   for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    # Highlight paths if provided
    if paths != [None]:
        for path in paths:
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="red", width=2)
        plt.title("Building Layout with Ant Paths")
        plt.show()
    else:
        print('ANTS COULD NOT FIND EXIT')


#main
def ant_colony_optimization(graph, num_iterations, num_ants, start_node):
    best_path = None
    best_fitness = float('inf')

    for iteration in range(num_iterations):
        paths, path_lengths = simulate_ants(graph, start_node, num_ants)
        update_pheromones(paths, path_lengths)

        #gets best path for iteration
        for path, length in zip(paths, path_lengths):
            if length < best_fitness:
                best_fitness = length
                best_path = path

        print(f"Iteration {iteration + 1}: Best Path = {best_path}, Fitness Value = {best_fitness:.2f}")

    return best_path, best_fitness


# start position for all ants
start_node = 'corridor3'

#run
best_path, best_fitness = ant_colony_optimization(building_graph, num_iterations, num_ants, start_node)

#visualise
visualize_graph(building_graph, pheromones, [best_path])