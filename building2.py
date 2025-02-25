import random

#parameters
num_rooms = 1000
num_corridors = 300
num_exits = 10
max_connections_per_room = 5

#generate nodes
rooms = [f"room{i}" for i in range(1, num_rooms + 1)]
corridors = [f"corridor{i}" for i in range(1, num_corridors + 1)]
exits = [f"exit{i}" for i in range(1, num_exits + 1)]

nodes = rooms + corridors + exits


edges = []

#rooms to corridors
for room in rooms:
    num_connections = random.randint(1, max_connections_per_room)
    connected_corridors = random.sample(corridors, num_connections)
    for corridor in connected_corridors:
        edges.append((room, corridor, {
            'distance': random.randint(1, 10),
            'risk': random.randint(1, 5)
        }))

#corridors to corridors or exits
for corridor in corridors:
    num_connections = random.randint(1, max_connections_per_room)
    connected_nodes = random.sample(corridors + exits, num_connections)
    for node in connected_nodes:
        if node != corridor:  # Avoid self-loops
            edges.append((corridor, node, {
                'distance': random.randint(1, 10),
                'risk': random.randint(1, 5)
            }))

#rooms to exits
for _ in range(num_rooms // 10):
    room = random.choice(rooms)
    exit_node = random.choice(exits)
    edges.append((room, exit_node, {
        'distance': random.randint(5, 20),
        'risk': random.randint(1, 3)
    }))

#pheromone and heuristic initialization
pheromones = {(edge[0], edge[1]): 1.0 for edge in edges}
heuristics = {(edge[0], edge[1]): 1 / (edge[2]['distance'] + edge[2]['risk']) for edge in edges}