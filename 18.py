from collections import deque, namedtuple
from input import read_input


Step = namedtuple('Step', ['dir', 'dist', 'color'])
Pos = namedtuple('Pos', ['i', 'j'])

plan = []
for _line in read_input(18):
    direction, _distance, _color = _line.split(' ')
    hexadecimal = f'{_color[2:-1]}'
    plan.append(Step(direction, int(_distance), hexadecimal))

dig_vector = {
    'U': Pos(-1, 0),
    'D': Pos(1, 0),
    'L': Pos(0, -1),
    'R': Pos(0, 1),
}

def add(a, b):
    return Pos(a.i + b.i, a.j + b.j)

def dig(plan):
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

print('Part 2: ', calculate_lava_volume(dig(correct_plan(plan)))) #
