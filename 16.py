import copy
from collections import deque, namedtuple
from input import read_input

Pos = namedtuple('Pos', ['i', 'j'])

Tile = namedtuple('Tile', ['type', 'beam_paths'])
# type in ['.', '|', '-', '/', '\\']
# beams in ['>', '<', 'v', '^']

sample_input = [
    '.|...\\....',
    '|.-.\\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....',
]
contraption = []
for i, row in enumerate(read_input(16)):
    contraption.append([])
    for _, tile_type in enumerate(row):
        contraption[i].append(Tile(tile_type, list()))

beam_vector = {
    '>': Pos(0, 1),
    '<': Pos(0, -1),
    'v': Pos(1, 0),
    '^': Pos(-1, 0),
}
beam_direction = {vector: direction for direction, vector in beam_vector.items()}

Beam = namedtuple('Beam', ['direction', 'pos'])

def add(a, b):
    return Pos(a.i + b.i, a.j + b.j)

def step_beam_head(tile_type, beam):
    if tile_type == '.':
        return [Beam(beam.direction, add(beam.pos, beam_vector[beam.direction]))]

    elif tile_type == '|':
        if beam.direction in ('>', '<'):
            return [
                Beam('v', add(beam.pos, beam_vector['v'])),
                Beam('^', add(beam.pos, beam_vector['^'])),
            ]
        else:
            return [Beam(beam.direction, add(beam.pos, beam_vector[beam.direction]))]

    elif tile_type == '-':
        if beam.direction in ('v', '^'):
            return [
                Beam('>', add(beam.pos, beam_vector['>'])),
                Beam('<', add(beam.pos, beam_vector['<'])),
            ]
        else:
            return [Beam(beam.direction, add(beam.pos, beam_vector[beam.direction]))]

    elif tile_type == '/':
        i, j = beam_vector[beam.direction]
        bounce_vector = Pos(-j, -i)
        new_direction = beam_direction[bounce_vector]
        return [
            Beam(new_direction, add(beam.pos, bounce_vector))
        ]

    elif tile_type == '\\':
        i, j = beam_vector[beam.direction]
        bounce_vector = Pos(j, i)
        new_direction = beam_direction[bounce_vector]
        return [
            Beam(new_direction, add(beam.pos, bounce_vector)),
        ]

    else:
        assert False

def run_contraption(contraption, initial_beam):
    contraption = copy.deepcopy(contraption)
    active_beam_heads = deque([initial_beam])

    rows = len(contraption)
    cols = len(contraption[0])

    while active_beam_heads:
        beam = active_beam_heads.popleft()

        beam_pos = beam.pos
        i, j = beam_pos

        if i < 0 or i >= rows or j < 0 or j >= cols:
            # beam has hit the boundary
            continue

        if beam.direction in contraption[i][j].beam_paths:
            # beam has traveled through before already
            continue
        contraption[i][j].beam_paths.append(beam.direction)

        next_beam_heads = step_beam_head(contraption[i][j].type, beam)
        active_beam_heads.extend(next_beam_heads)

    return contraption

def count_energized_tiles(contraption):
    energized_tiles = 0
    for row in contraption:
        for tile in row:
            if len(tile.beam_paths) > 0:
                energized_tiles += 1
    return energized_tiles

def print_contraption(contraption, print_energized=False):
    for row in contraption:
        row_to_print = []
        for tile in row:
            if print_energized and len(tile.beam_paths) > 0:
                row_to_print.append('#')
            elif print_energized:
                row_to_print.append('.')

            elif tile.type in ('|', '-', '/', '\\'):
                row_to_print.append(tile.type)
            elif len(tile.beam_paths) == 0:
                row_to_print.append(tile.type)
            elif len(tile.beam_paths) == 1:
                row_to_print.append(tile.beam_paths[0])
            elif len(tile.beam_paths) > 1:
                row_to_print.append(str(len(tile.beam_paths)))
        print(''.join(row_to_print))

# print_contraption(contraption)
finished_contraption = run_contraption(contraption, Beam('>', Pos(0, 0)))
# print_contraption(finished_contraption)
# print_contraption(finished_contraption, print_energized=True)
print('Part 1: ', count_energized_tiles(finished_contraption)) # 8901

def find_max_energy(contraption):
    max_energy = 0
    rows = len(contraption)
    cols = len(contraption[0])

    for j in range(cols):
        finished_contraption = run_contraption(contraption, Beam('v', Pos(0, j)))
        energy = count_energized_tiles(finished_contraption)
        max_energy = max(energy, max_energy)

        finished_contraption = run_contraption(contraption, Beam('^', Pos(rows - 1, j)))
        energy = count_energized_tiles(finished_contraption)
        max_energy = max(energy, max_energy)

    for i in range(rows):
        finished_contraption = run_contraption(contraption, Beam('>', Pos(i, 0)))
        energy = count_energized_tiles(finished_contraption)
        max_energy = max(energy, max_energy)

        finished_contraption = run_contraption(contraption, Beam('<', Pos(i, cols - 1)))
        energy = count_energized_tiles(finished_contraption)
        max_energy = max(energy, max_energy)

    return max_energy

print('Part 2: ', find_max_energy(contraption)) # 9064
