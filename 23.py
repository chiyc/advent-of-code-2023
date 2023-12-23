from collections import deque, namedtuple
from input import read_input


grid = []
for row in read_input(23):
    grid.append(list(row))

Pos = namedtuple('Pos', ['i', 'j'])
Path = namedtuple('Path', ['head', 'steps', 'prev'])

def find_start(grid):
    start_i = 0
    start_j = grid[start_i].index('.')
    return Pos(start_i, start_j)

def find_end(grid):
    end_i = len(grid) - 1
    end_j = grid[end_i].index('.')
    return Pos(end_i, end_j)

def find_longest_path_with_icy_slopes(grid):
    rows = len(grid)
    end_i, end_j = find_end(grid)
    end_pos = Pos(end_i, end_j)

    max_steps = {}
    start_i, start_j = find_start(grid)
    next = deque([Path(Pos(start_i, start_j), 0, [])])
    while next:
        path = next.popleft()
        i, j = path.head
        if i < 0 or i >= rows:
            continue

        if grid[i][j] == '#':
            continue

        if path.head in path.prev:
            continue

        if path.head in max_steps and max_steps[path.head] > len(path.prev):
            continue

        max_steps[path.head] = len(path.prev)

        if path.head == end_pos:
            continue

        next_steps = len(path.prev) + 1
        next_prev = path.prev + [path.head]
        if grid[i][j] == '^':
            next.append(Path(Pos(i - 1, j), next_steps, next_prev))

        elif grid[i][j] == 'v':
            next.append(Path(Pos(i + 1, j), next_steps, next_prev))

        elif grid[i][j] == '<':
            next.append(Path(Pos(i, j - 1), next_steps, next_prev))

        elif grid[i][j] == '>':
            next.append(Path(Pos(i, j + 1), next_steps, next_prev))

        else:
            next.extend([
                Path(Pos(i - 1, j), next_steps, next_prev),
                Path(Pos(i + 1, j), next_steps, next_prev),
                Path(Pos(i, j - 1), next_steps, next_prev),
                Path(Pos(i, j + 1), next_steps, next_prev),
            ])

    return max_steps[end_pos]

print('Part 1: ', find_longest_path_with_icy_slopes(grid)) # 2326
# print('Part 2: ', find_longest_path(grid, icy_slopes = False)) # too slow

Edge = namedtuple('Edge', ['head', 'weight'])

def find_intersections(grid):
    intersections = []
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            crossroads = [
                grid[i - 1][j],
                grid[i + 1][j],
                grid[i][j - 1],
                grid[i][j + 1],
            ]

            if (
                grid[i][j] in ('.', '^', 'v', '<', '>')
                and len(list(filter(lambda tile: tile in ('.', '^', 'v', '<', '>'), crossroads))) > 2
            ):
                intersections.append(Pos(i, j))
    return intersections

def build_node_edges(starting_node, grid, nodes):
    edges = []
    next = deque([Path(starting_node, 0, [])])
    while next:
        path = next.popleft()
        i, j = path.head

        if i < 0 or i >= len(grid):
            continue

        if grid[i][j] == '#':
            continue

        if path.head in path.prev:
            continue

        if path.head != starting_node and path.head in nodes:
            edges.append(Edge(path.head, path.steps))
            continue

        next_steps = path.steps + 1
        next_prev = path.prev + [path.head]
        next.extend([
            Path(Pos(i - 1, j), next_steps, next_prev),
            Path(Pos(i + 1, j), next_steps, next_prev),
            Path(Pos(i, j - 1), next_steps, next_prev),
            Path(Pos(i, j + 1), next_steps, next_prev),
        ])
    return edges

def build_weighted_graph(grid):
    graph = {}

    intersections = find_intersections(grid)
    nodes = intersections + [find_start(grid), find_end(grid)]
    for node in nodes:
        if node not in graph:
            graph[node] = []
        edges = build_node_edges(node, grid, nodes)
        graph[node] = edges
        for edge in edges:
            if edge not in graph[node]:
                graph[node].append(edge)
            other_node = edge.head
            if other_node not in graph:
                graph[other_node] = []
            if Edge(node, edge.weight) not in graph[other_node]:
                graph[other_node].append(Edge(node, edge.weight))

    return graph

def find_longest_path_on_graph(graph, start, end):
    max_steps = {}
    next = deque([Path(start, 0, [])])
    while next:
        path = next.popleft()

        if path.head in path.prev:
            continue

        if path.head == end:
            if end not in max_steps:
                max_steps[end] = path.steps
            elif path.steps > max_steps[end]:
                max_steps[end] = path.steps
            continue

        next_prev = path.prev + [path.head]
        next.extend([
            Path(edge.head, path.steps + edge.weight, next_prev)
            for edge in graph[path.head]
        ])
    return max_steps[end]

graph = build_weighted_graph(grid)
print('Part 2: ', find_longest_path_on_graph(graph, find_start(grid), find_end(grid))) # 6574
