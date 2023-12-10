from collections import deque, namedtuple
from input import read_input


tiles = [list(line) for line in read_input(10)]

# Node is used as node ID and location
Node = namedtuple('Node', ['i', 'j'])

pipe_edges = {
    '|': [Node(-1, 0), Node(1, 0)],
    '-': [Node(0, -1), Node(0, 1)],
    'L': [Node(-1, 0), Node(0, 1)],
    'J': [Node(-1, 0), Node(0, -1)],
    '7': [Node(1, 0), Node(0, -1)],
    'F': [Node(1, 0), Node(0, 1)],
}

graph = {}
start_node = None

# Build adjacency list from 2D tiles in 2 stages

# Stage 1: Add edges from each node depending its tile
for i, _line in enumerate(tiles):
    for j, tile in enumerate(list(_line)):
        node = Node(i, j)
        graph[node] = []

        if tile == 'S':
            # Save node ID for starting node to be used later
            start_node = node

        elif tile in pipe_edges:
            # For each pipe node, add an edge to its neighbors
            edges = [Node(node.i + edge.i, node.j + edge.j) for edge in pipe_edges[tile]]
            graph[node].extend(edges)

# Stage 2: Remove any edges that are not reciprocated. Handle special case for S.
for node, neighbors in graph.items():
    for neighbor in neighbors:
        if neighbor not in graph:
            # Edge goes out-of-bounds, so remove the edge
            neighbors.remove(neighbor)

        elif node not in graph[neighbor]:
            # Edge is not reciprocated by neighboring tile
            neighbor_tile = tiles[neighbor.i][neighbor.j]

            if neighbor_tile == 'S':
                # S is a special case that was not initialized with edges but will reciprocate
                graph[neighbor].append(node)
            else:
                neighbors.remove(neighbor)

def bfs(graph, start_node):
    visited = {node: False for node in graph.keys()}
    distance_from_start = {node: -1 for node in graph.keys()}

    distance_from_start[start_node] = 0
    next_nodes = deque([start_node])
    while next_nodes:
        node = next_nodes.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distance_from_start[neighbor] = distance_from_start[node] + 1
                next_nodes.append(neighbor)

    return distance_from_start

print('Part 1: ', max(bfs(graph, start_node).values())) # 6778
