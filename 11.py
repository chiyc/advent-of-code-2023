from collections import deque, namedtuple
from input import read_input


Node = namedtuple('Node', ['i', 'j'])

original_grid = [list(row) for row in read_input(11)]

def expand_universe(universe_grid):
    grid = []
    for i, row in enumerate(universe_grid):
        grid.append(list(row))
        if all([c == '.' for c in row]):
            grid.append(list(row))

    j = 0
    while j < len(grid[0]):
        if all([grid[i][j] == '.' for i in range(len(grid))]):
            for i in range(len(grid)):
                grid[i].insert(j, '.')
            j += 2
        else:
            j += 1
    return grid

def get_galaxy_nodes(universe_grid):
    galaxies = []
    for i, row in enumerate(universe_grid):
        for j, c in enumerate(row):
            if c == '#':
                galaxies.append(Node(i, j))
    return galaxies

def get_shortest_path_length(start, end):
    return abs(start.i - end.i) + abs(start.j - end.j)

def sum_shortest_path_lengths(universe_grid):
    galaxies = get_galaxy_nodes(universe_grid)

    pair_distances = []
    for p, galaxy in enumerate(galaxies):
        for q in range(p + 1, len(galaxies)):
            pair_distances.append(get_shortest_path_length(galaxy, galaxies[q]))

    return sum(pair_distances)

print('Part 1: ', sum_shortest_path_lengths(expand_universe(original_grid))) # 9550717

def get_empty_rows(universe_grid):
    result = []
    for i, row in enumerate(universe_grid):
        if all([c == '.' for c in row]):
            result.append(i)
    return result

def get_empty_cols(universe_grid):
    result = []
    j = 0
    for j, _ in enumerate(universe_grid[0]):
        if all([universe_grid[i][j] == '.' for i, _ in enumerate(universe_grid)]):
            result.append(j)
    return result

def sum_shortest_path_lengths_in_mega_expanded_universe(original_universe):
    empty_rows = get_empty_rows(original_universe)
    empty_cols = get_empty_cols(original_universe)
    galaxies = get_galaxy_nodes(original_universe)

    sum_of_distances = 0
    for p, start in enumerate(galaxies):
        for q in range(p + 1, len(galaxies)):
            end = galaxies[q]
            expanded_rows = len([i for i in empty_rows if start.i < i < end.i or start.i > i > end.i])
            expanded_cols = len([j for j in empty_cols if start.j < j < end.j or start.j > j > end.j])
            distance = get_shortest_path_length(start, end) + expanded_rows * 999999 + expanded_cols * 999999
            sum_of_distances += distance
    return sum_of_distances

print('Part 2: ', sum_shortest_path_lengths_in_mega_expanded_universe(original_grid)) # 648458253817
