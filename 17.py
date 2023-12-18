from copy import deepcopy
from collections import deque, namedtuple
from input import read_input


grid = []
for row in read_input(17):
    grid.append(list(map(int, row)))

Pos = namedtuple('Pos', ['i', 'j'])
Path = namedtuple('Path', ['pos', 'heat', 'prev'])

path_vector = {
    '^': Pos(-1, 0),
    'v': Pos(1, 0),
    '<': Pos(0, -1),
    '>': Pos(0, 1),
}
path_direction = {vector: direction for direction, vector in path_vector.items()}

def add(a, b):
    return Pos(a.i + b.i, a.j + b.j)

def step_path(path):
    next_positions = [
        add(path.pos, path_vector['^']),
        add(path.pos, path_vector['v']),
        add(path.pos, path_vector['<']),
        add(path.pos, path_vector['>']),
    ]

    if len(path.prev) > 0:
        # Can't go backwards
        next_positions.remove(path.prev[-1])

    if len(path.prev) >= 3:
        # Remove the path going to the fourth consecutive straight line
        i, j = path.pos
        i_m3, j_m3 = path.prev[-3]
        if abs(i - i_m3) == 3 or abs(j - j_m3) == 3:
            i_m1, j_m1 = path.prev[-1]
            forward_vector = Pos(i - i_m1, j - j_m1)
            forward_pos = add(path.pos, forward_vector)
            next_positions.remove(forward_pos)

    return next_positions

def find_minimum_heat_path(grid):
    # Kind of cheat at shrinking the input by filling out the center area that contains 9s.
    # Below, we terminate the path when we hit a 9 because the optimal path goes
    # around that area.
    for i, row in enumerate(grid):
        if 9 in row:
            first_9 = row.index(9)
            last_9_exclusive = len(row) - list(reversed(row)).index(9)
            row[first_9 : last_9_exclusive] = [9] * (last_9_exclusive - first_9)

    rows = len(grid)
    cols = len(grid[0])

    # For each position, we have a map of the optimal heat values seen so far. These
    # values are keyed based on how we entered the block. (direction, consecutive_straight_steps)
    minimum_heat = [
        [{} for _ in range(cols)] for _ in range(rows)
    ]

    # Used to store the final path to the end
    minimum_heat_path = []
    # Used to track the minimum heat path to the end
    final_minimum_heat = None

    starting_point = Path(Pos(0,0), 0, [])
    active_paths = deque([Path(position, 0, [starting_point.pos]) for position in step_path(starting_point)])
    while active_paths:
        path = active_paths.popleft()
        i, j = path.pos

        if i < 0 or i >= rows or j < 0 or j >= cols:
            continue

        if path.pos in path.prev:
            # There's no way this can be a minimum heat path since a loop means
            # a more direct path exists
            continue

        # The optimal path won't go through a 9
        if grid[i][j] >= 9:
            continue

        # Accumulated heat loss so far
        path_heat = path.heat + grid[i][j]

        if path_heat > 9 * (i + j):
            # This is probably a sub-optimal path since it's worse than
            # the worst case values of just blowing through 9s
            continue

        if len(path.prev) >= 3:
            # In order to find the optimal path, we can't just compare the accumulative
            # heat at a given position. It must also be compared against heat loss values from
            # paths that arrived at the position the same way. The way a path arrived is based
            # on incoming direction and consecutive straight steps taken.
            straight_steps = 1
            m1 = path.prev[-1]
            delta_m1 = Pos(i - m1.i, j - m1.j)

            m2 = path.prev[-2]
            delta_m2 = Pos(m1.i - m2.i, m1.j - m2.j)
            if delta_m2 == delta_m1:
                straight_steps += 1

            m3 = path.prev[-3]
            delta_m3 = Pos(m2.i - m3.i, m2.j - m3.j)
            if delta_m3 == delta_m2 and delta_m2 == delta_m1:
                straight_steps += 1

            heat_key = (delta_m1, straight_steps)

            if heat_key not in minimum_heat[i][j] or path_heat < minimum_heat[i][j][heat_key]:
                minimum_heat[i][j][heat_key] = path_heat
            else:
                continue

        # This is the next path.prev list with the current position
        path_prev = path.prev + [path.pos]

        if path.pos == Pos(rows - 1, cols - 1):
            # Tracking this isn't necessary, but I'm using it for visualizing the
            # path for printing
            if final_minimum_heat is None or path_heat < final_minimum_heat:
                final_minimum_heat = path_heat
                minimum_heat_path = path_prev
            continue

        next_paths = [
            Path(next_pos, path_heat, path_prev)
            for next_pos in step_path(path)
        ]
        active_paths.extend(next_paths)

    return min(minimum_heat[-1][-1].values()), minimum_heat_path

def print_grid(grid, final_path):
    grid_to_print = deepcopy(grid)
    print('Printing final path')
    print('=====')
    print(f'{len(final_path)} steps')
    print('=====')
    # print(final_path)

    path_to_print = []
    for step in range(1, len(final_path)):
        pos = final_path[step]
        i, j = pos
        i_m1, j_m1 = final_path[step - 1]
        pos_heat = grid[i][j]
        grid_to_print[i][j] = path_direction[Pos(i - i_m1, j - j_m1)]
        path_to_print.append(grid_to_print[i][j] + str(pos_heat))

    print(','.join(path_to_print))

    print('=====')
    for row in grid_to_print:
        print(''.join([str(tile) for tile in row]))
    print('=====')

minimum_heat, minimum_heat_path = find_minimum_heat_path(grid)
print('Part 1: ', minimum_heat) # 1076, takes just over 5 minutes to run
# print_grid(grid, minimum_heat_path)
