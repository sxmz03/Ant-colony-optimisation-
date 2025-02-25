# Nodes of the building
nodes = [
    'room1', 'room2', 'room3', 'room4', 'room5',
    'corridor1', 'corridor2', 'corridor3', 'corridor4',
    'corridor5', 'exit1', 'exit2'
]

# Edges of the building with distances and risks
edges = [
    #room to corridors
    ('room1', 'corridor1', {'distance': 3, 'risk': 2}),
    ('room2', 'corridor1', {'distance': 4, 'risk': 1}),
    ('room3', 'corridor2', {'distance': 2, 'risk': 1}),
    ('room4', 'corridor3', {'distance': 5, 'risk': 3}),
    ('room5', 'corridor4', {'distance': 4, 'risk': 2}),

    #corridor connections
    ('corridor1', 'corridor2', {'distance': 6, 'risk': 1}),
    ('corridor2', 'corridor3', {'distance': 4, 'risk': 2}),
    ('corridor3', 'corridor4', {'distance': 5, 'risk': 2}),
    ('corridor4', 'corridor5', {'distance': 3, 'risk': 1}),
    ('corridor5', 'corridor1', {'distance': 7, 'risk': 3}),

    #corridors to exits
    ('corridor2', 'exit1', {'distance': 3, 'risk': 1}),
    ('corridor4', 'exit2', {'distance': 4, 'risk': 1}),
    ('corridor5', 'exit2', {'distance': 2, 'risk': 2}),

    #other paths
    ('room1', 'room3', {'distance': 8, 'risk': 4}),
    ('room2', 'room4', {'distance': 7, 'risk': 3}),
    ('room5', 'room3', {'distance': 6, 'risk': 3}),
    ('corridor1', 'room5', {'distance': 5, 'risk': 1}),
]
num_exits = 2
#pheromone and heurstics initialization
pheromones = {(edge[0], edge[1]): 1.0 for edge in edges}
heuristics = {(edge[0], edge[1]): 1 / (edge[2]['distance'] + edge[2]['risk']) for edge in edges}