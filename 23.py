from collections import deque, namedtuple
from input import read_input


grid = []
for row in read_input(23):
    grid.append(list(row))

Pos = namedtuple('Pos', ['i', 'j'])
Path = namedtuple('Path', ['head', 'steps', 'prev'])

def longest_path_to_end(grid, icy_slopes=True):
    rows = len(grid)
    cols = len(grid[0])
    end_i = rows - 1
    end_j = grid[end_i].index('.')
    end_pos = Pos(end_i, end_j)

    max_steps = {}

    start_i = 0
    start_j = grid[start_i].index('.')
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
        if icy_slopes and grid[i][j] == '^':
            next.append(Path(Pos(i - 1, j), next_steps, next_prev))

        elif icy_slopes and grid[i][j] == 'v':
            next.append(Path(Pos(i + 1, j), next_steps, next_prev))

        elif icy_slopes and grid[i][j] == '<':
            next.append(Path(Pos(i, j - 1), next_steps, next_prev))

        elif icy_slopes and grid[i][j] == '>':
            next.append(Path(Pos(i, j + 1), next_steps, next_prev))

        else:
            next.extend([
                Path(Pos(i - 1, j), next_steps, next_prev),
                Path(Pos(i + 1, j), next_steps, next_prev),
                Path(Pos(i, j - 1), next_steps, next_prev),
                Path(Pos(i, j + 1), next_steps, next_prev),
            ])

    return max_steps[end_pos]

print('Part 1: ', longest_path_to_end(grid)) # 2326
print('Part 2: ', longest_path_to_end(grid, icy_slopes = False)) # too slow
