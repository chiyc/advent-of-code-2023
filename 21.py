from collections import deque, namedtuple
from input import read_input


grid = []
for row in read_input(21):
    grid.append(list(row))

def find_starting_point(grid):
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == 'S':
                return (i, j)
    assert False

Path = namedtuple('Path', ['position', 'steps'])

def step_to_garden(grid, exact_steps=64, infinite=False):
    rows = len(grid)
    cols = len(grid[0])

    grid_steps = {}
    start = find_starting_point(grid)
    next = deque([Path(start, 0)])
    while next:
        position, steps = next.popleft()
        i, j = position

        if steps > exact_steps:
            continue

        if not infinite and (i < 0 or i >= rows or j < 0 or j >= cols):
            continue

        if position in grid_steps:
            continue

        if i < 0 or i >= rows or j < 0 or j >= cols:
            infinite_i = i % rows
            infinite_j = j % rows
            tile = grid[infinite_i][infinite_j]
        else:
            tile = grid[i][j]

        if tile == '#':
            continue

        grid_steps[position] = steps

        next.extend([
            Path((i, j-1), steps + 1),
            Path((i, j+1), steps + 1),
            Path((i-1, j), steps + 1),
            Path((i+1, j), steps + 1),
        ])

    reached_garden_count = 0
    for position, steps in grid_steps.items():
        if steps % 2 == exact_steps % 2:
            reached_garden_count += 1
    return reached_garden_count

print('Part 1: ', step_to_garden(grid, exact_steps=64)) # 3847
print('Part 2: ', step_to_garden(grid, exact_steps=26501365, infinite=True)) # runs too slowly
