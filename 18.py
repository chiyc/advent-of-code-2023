import operator
from collections import deque, namedtuple
from input import read_input
from intervaltree import IntervalTree

Step = namedtuple('Step', ['dir', 'dist', 'color'])
Pos = namedtuple('Pos', ['i', 'j'])

plan = []
for _line in read_input(18):
    direction, _distance, _color = _line.split(' ')
    hexadecimal = f'{_color[2:-1]}'
    plan.append(Step(direction, int(_distance), hexadecimal))

def add(a, b):
    return Pos(a.i + b.i, a.j + b.j)

# Turns the plan into a 2D grid of trenches
def dig(plan):
    dig_vector = {
        'U': Pos(-1, 0),
        'D': Pos(1, 0),
        'L': Pos(0, -1),
        'R': Pos(0, 1),
    }

    trenches = {}

    position = Pos(0, 0)
    trenches[position] = '#'

    min_i, max_i = 0, 0
    min_j, max_j = 0, 0

    for step in plan:
        vector = dig_vector[step.dir]
        for _ in range(step.dist):
            position = add(position, vector)
            trenches[position] = '#'

        min_i = min(position.i, min_i)
        max_i = max(position.i, max_i)
        min_j = min(position.j, min_j)
        max_j = max(position.j, max_j)

    # Padding array by 1 square
    grid = [
        ['.' for _ in range(max_j - min_j + 3)]
        for _ in range(max_i - min_i + 3)
    ]

    for position in trenches.keys():
        i = position.i - min_i + 1
        j = position.j - min_j + 1
        grid[i][j] = '#'

    return grid

def calculate_lava_volume(grid):

    # First 'fill' in the ground outside the trench
    def bfs_outside():
        rows = len(grid)
        cols = len(grid[0])

        visited = {}
        next = deque([Pos(0, 0)])
        while next:
            position = next.popleft()
            i, j = position
            if position in visited:
                continue
            if i < 0 or i >= rows or j < 0 or j >= cols:
                continue
            if grid[i][j] == '#':
                continue
            visited[position] = True
            grid[i][j] = ' '
            next_positions = [
                add(position, Pos(-1, 0)),
                add(position, Pos(1, 0)),
                add(position, Pos(0, -1)),
                add(position, Pos(0, 1)),
            ]
            next.extend(next_positions)

    bfs_outside()

    # Any untouched ground counts as inside the trench
    volume = 0
    for row in grid:
        for tile in row:
            if tile in ('#', '.'):
                volume += 1
    return volume

print('Part 1: ', calculate_lava_volume(dig(plan))) # 36679

def correct_plan(plan):
    hex_dir = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
    }
    return list(map(lambda step: Step(hex_dir[step.color[-1]], int(step.color[:-1], 16), step.color),
                    plan))

def calculate_huge_lava_volume(plan):
    # Use x, y coordinates instead of i, j
    dig_vector = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0),
    }



    x, y = 0, 1 # Used for indexing the point tuple

    # Maintain min_y and max_y for knowing the iteration range
    min_y, max_y = 0, 0

    # The two following data structures are used to calculate volume at the end.
    # We'll be scanning row-by-row to add up the enclosed area.

    # Record turning points in each row
    #   Key by row number (y value)
    #   Value is a list of tuples made up of x position and corner type (23, 'F')
    row_corners = {}

    # Use an interval tree to store any vertical lines
    #   Key by y values that the vertical line goes through
    #   Value is the x position for the vertical line
    vertical_lines = IntervalTree()

    # We'll record the orientation leaving and returning to the start position to
    # determine the type of corner at that position
    start_edges = []

    # We take the trench lines at each step and turn them into Day 10 style pipes.
    prev_step_dir = None
    position = (0, 0)
    for i, step in enumerate(plan):
        if i > 0:
            prev_step_dir = plan[i - 1].dir

        if position[y] not in row_corners:
            row_corners[position[y]] = []

        if position == (0, 0):
            start_edges.append(step.dir)

        # Determine the type of corner based on the previous and current step
        tail_corner = {
            'U': {'L': '7', 'R': 'F'},
            'D': {'L': 'J', 'R': 'L'},
            'L': {'U': 'L', 'D': 'F'},
            'R': {'U': 'J', 'D': '7'},
            None: {},
        }[prev_step_dir].get(step.dir)
        if tail_corner is not None:
            row_corners[position[y]].append((position[x], tail_corner))

        next_position = (
            position[x] + step.dist * dig_vector[step.dir][x],
            position[y] + step.dist * dig_vector[step.dir][y],
        )

        # Note the interval is exclusive of both end positions, which we'll use to
        # record the corner type
        if step.dir == 'U':
            vertical_lines[position[y]+1 : next_position[y]] = position[x]
        elif step.dir == 'D':
            vertical_lines[next_position[y]+1 : position[y]] = position[x]

        min_y = min(next_position[y], min_y)
        max_y = max(next_position[y], max_y)

        if next_position == (0, 0):
            start_edges.append(step.dir)

        position = next_position

    start_corner = {
        'U': {'L': 'L', 'R': 'J'},
        'D': {'L': 'F', 'R': '7'},
        'L': {'U': '7', 'D': 'J'},
        'R': {'U': 'F', 'D': 'L'},
    }[start_edges[0]][start_edges[1]]
    row_corners[0].append((0, start_corner))

    volume = 0
    # Now we scan row by row to determine the lava volume contributed by that row
    for row in range(min_y, max_y + 1):
        # We start from the left and go right, counting any tiles that we determine are inside the trench
        verticals_in_row = list(map(lambda interval: (interval.data, '|'), vertical_lines[row]))
        corners_in_row = row_corners.get(row, [])
        pieces = sorted(verticals_in_row + corners_in_row, key=lambda item: item[0])

        inside = False # Track whether we've crossed inside the trench or outside
        last_piece = None
        last_col = None
        for col, piece in pieces:
            if piece == '|':
                if inside:
                    volume += col - last_col
                else:
                    # If we're outside, we just count the first '|' as we cross inside, which
                    # won't be counted in the other cases
                    volume += 1
                inside = not inside

            elif piece in ('F', 'L'):
                if inside:
                    volume += col - last_col
                else:
                    # Same as above, we just count the first corner as we cross inside, which
                    # won't be counted in the other cases
                    volume += 1
                last_piece = piece

            elif piece in ('J', '7'):
                volume += col - last_col

                crossed = {
                    'F': {'J': True, '7': False},
                    'L': {'J': False, '7': True},
                }[last_piece][piece]
                if crossed:
                    inside = not inside

            last_col = col
            last_piece = piece

    return volume

# print('Part 1: ', calculate_huge_lava_volume(plan)) # 36679
corrected_plan = correct_plan(plan)
print('Part 2: ', calculate_huge_lava_volume(corrected_plan)) # 88007104020978, takes 3 minutes to run
