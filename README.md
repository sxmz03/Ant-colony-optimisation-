# Ant Colony Optimisation — Building Evacuation

An implementation of Ant Colony Optimisation (ACO) to find the fastest and safest evacuation path from a building, modelling corridors and exits as a weighted directed graph.

## Overview

This project simulates ant agents navigating a building graph to discover optimal escape routes. Each path is scored by a fitness function that combines distance and risk, with pheromone trails reinforcing the best routes over multiple iterations.

## Features

- ACO with configurable pheromone importance (α) and heuristic importance (β)
- Fitness function combining distance and risk per edge
- Probabilistic next-step selection based on pheromone and heuristic weights
- Pheromone evaporation and reinforcement across iterations
- Graph visualisation using NetworkX and Matplotlib
- Two building layouts included (`building1.py`, `building2.py`)

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| NetworkX | Directed graph representation of building |
| Matplotlib | Path and graph visualisation |

## Algorithm Parameters

```python
num_ants = 10
num_iterations = 10
alpha = 0.5        # Pheromone importance
beta = 0.5         # Heuristic importance
evaporation_rate = 0.8
Q = 1              # Pheromone deposit constant
```

## Setup

```bash
pip install networkx matplotlib
```

Run the simulation:

```bash
python main.py
```

Switch between building layouts by editing the import at the top of `main.py`:

```python
import building1  # or building2
```

## How It Works

1. Ants start at a designated node and traverse edges probabilistically
2. Probability of choosing the next node is proportional to pheromone level and heuristic value
3. After all ants complete their paths, pheromones evaporate and are re-deposited based on path quality
4. The best path (lowest combined distance + risk) is returned after all iterations
