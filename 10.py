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

distance_from_start = bfs(graph, start_node)
print('Part 1: ', max(distance_from_start.values())) # 6778

# Part 2

# Clean up pipes that are not part of the loop
for node in graph:
    tile = tiles[node.i][node.j]
    if distance_from_start[node] == -1 and tile != '.':
        tiles[node.i][node.j] = '.' # Turn them into ground
        # Don't bother editing the adjacency list since we won't use it anymore

# Need to turn start_node 'S' into a pipe for the next step
for pipe, edges in pipe_edges.items():
    if all([
        Node(neighbor.i - start_node.i, neighbor.j - start_node.j) in edges
        for neighbor in graph[start_node]
    ]):
        tiles[start_node.i][start_node.j] = pipe

# Stretch the graph in both dimensions, which will create gaps between parallel pipes.
# Set those new tile gaps as a single space character: ' '
stretched_tiles = []
for row in tiles:
    stretched_row = []
    next_row = []
    for tile in row:
        stretched_row.append(tile)

        # Stretch pipes vertically
        if tile in ['|', '7', 'F']:
            next_row.append('|')
        else:
            next_row.append(' ')

        # Stretch pipes horizontally
        if tile in ['-', 'L', 'F']:
            stretched_row.append('-')
            next_row.append(' ')
        else:
            stretched_row.append(' ')
            next_row.append(' ')

    stretched_tiles.append(stretched_row)
    stretched_tiles.append(next_row)

rows = len(stretched_tiles)
cols = len(stretched_tiles[0])

# BFS from Node(0,0) to find all '.' or ' ' tiles reachable from the outside
# Don't bother creating adjacency list, just traverse across ' ' or '.' on stretched_tiles

next_nodes = deque([Node(0, 0)])
while next_nodes:
    node = next_nodes.popleft()
    i, j = node
    # Visited tiles are marked with 'x'
    if stretched_tiles[i][j] == 'x':
        continue

    possible_neighbors = [
        Node(i, j-1),
        Node(i, j+1),
        Node(i-1, j),
        Node(i+1, j),
    ]
    valid_neighbors = []
    for neighbor in possible_neighbors:
        if (
            0 <= neighbor.i < rows
            and 0 <= neighbor.j < cols
            and stretched_tiles[neighbor.i][neighbor.j] in [' ', '.']
        ):
            valid_neighbors.append(neighbor)

    stretched_tiles[i][j] = 'x' # Mark as visited
    next_nodes.extend(valid_neighbors)

# Then count the remaining '.' ground tiles that were not visited, those are the enclosed tiles

untouched_ground_count = 0
for row in stretched_tiles:
    for tile in row:
        if tile == '.':
            untouched_ground_count += 1

print('Part 2: ', untouched_ground_count) # 433


# Trying Mav's crossing method

def is_inside(tiles, node):
    crossings = 0
    ni, nj = node
    last_bend = None
    # Hop east from the current tile and count full pipe crossings
    for j in range(nj, len(tiles[0])):
        tile = tiles[ni][j]
        if tile == '|':
            crossings += 1

        elif tile in ['F', 'L']:
            last_bend = tile

        elif tile in ['J', '7']:
            # Count as a crossing depending on what sort of bend last seen
            crossings += {
                'F': {'J': 1, '7': 0},
                'L': {'J': 0, '7': 1},
            }[last_bend][tile]
            last_bend = None
    # Odd number of crossings means we were inside the loop
    return crossings % 2 == 1

inside_count = 0
for i, row in enumerate(tiles):
    for j, tile in enumerate(row):
        if tile == '.' and is_inside(tiles, Node(i, j)):
            inside_count += 1

print('Part 2: ', inside_count)
