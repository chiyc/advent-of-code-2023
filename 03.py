from collections import namedtuple
from input import read_input


Loc = namedtuple('Loc', ['i',  'j0', 'j1']) # exclusive j1

def row_numbers(schematic, i):
    row = schematic[i]
    j0, j1 = 0, 0
    while j0 < len(row) and j1 < len(row):
        if row[j0].isdigit():
            j1 = j0 + 1
            while j1 < len(row) and row[j1].isdigit():
                j1 += 1
            yield Loc(i, j0, j1)
            j0 = j1
        else:
            j0 += 1

def get_number(schematic, num_loc):
    i, j0, j1 = num_loc
    return int(schematic[i][j0:j1])

def schematic_number_locs(schematic):
    numbers = []
    for i, schematic_row in enumerate(schematic):
        for num_loc in row_numbers(schematic, i):
            numbers.append(num_loc)
    return numbers

def is_symbol(c):
    return not c.isdigit() and c != '.'

def has_adjacent_symbol(schematic, num_loc):
    min_i, max_i = 0, len(schematic) - 1 # treat row indexes inclusively
    min_j, max_j = 0, len(schematic[0])

    i, j0, j1 = num_loc

    surrounding_points = []

    if i > min_i: # points above
        row = schematic[i-1]
        start, end = max(min_j, j0 - 1), min(max_j, j1 + 1)
        surrounding_points += list(row[start:end])

    if i < max_i: # points below
        row = schematic[i+1]
        start, end = max(min_j, j0 - 1), min(max_j, j1 + 1)
        surrounding_points += list(row[start:end])

    if j0 > min_j: # point to left
        surrounding_points.append(schematic[i][j0-1])

    if j1 < max_j: # point to right
        surrounding_points.append(schematic[i][j1])

    return any(map(is_symbol, surrounding_points))


# Part 2 functions

def schematic_gear_locs(schematic):
    gears = []
    for i, schematic_row in enumerate(schematic):
        for j, c in enumerate(schematic_row):
            if c == '*':
                gears.append(Loc(i, j, j+1))
    return gears

def schematic_numbers_by_row(num_locs):
    numbers_by_row = {}
    for num_loc in num_locs:
        i, _, _ = num_loc
        if i not in numbers_by_row:
            numbers_by_row[i] = []
        numbers_by_row[i].append(num_loc)
    return numbers_by_row

def get_number_at_loc(numbers_by_row, loc):
    i, j, _ = loc
    for num_loc in numbers_by_row.get(i, []):
        _, j0, j1 = num_loc
        if j0 <= j < j1:
            return num_loc

def get_adjacent_numbers(numbers_by_row, gear_loc):
    i, j, _ = gear_loc

    adjacent_numbers = set()
    adjacent_locs = [
        Loc(i-1, j-1, j),
        Loc(i-1, j,   j+1),
        Loc(i-1, j+1, j+2),
        Loc(i,   j-1, j),
        Loc(i,   j+1, j+2),
        Loc(i+1, j-1, j),
        Loc(i+1, j,   j+1),
        Loc(i+1, j+1, j+2),
    ]
    for loc in adjacent_locs:
        num_loc = get_number_at_loc(numbers_by_row, loc)
        if num_loc is not None:
            adjacent_numbers.add(num_loc)

    return adjacent_numbers


# Run script
schematic = []
for line in read_input(3):
    schematic.append(line)

part_numbers = []
num_locs = schematic_number_locs(schematic)

# Part 1
for num_loc in num_locs:
    if has_adjacent_symbol(schematic, num_loc):
        part_numbers.append(get_number(schematic, num_loc))

# Part 2
num_locs_by_row = schematic_numbers_by_row(num_locs)
gear_ratios = []
for gear_loc in schematic_gear_locs(schematic):
    print(gear_loc)
    adjacent_numbers = get_adjacent_numbers(num_locs_by_row, gear_loc)
    if len(adjacent_numbers) == 2:
        num0 = get_number(schematic, adjacent_numbers.pop())
        num1 = get_number(schematic, adjacent_numbers.pop())
        gear_ratios.append(num0*num1)

print('Part 1: ', sum(part_numbers)) # 553079
print('Part 2: ', sum(gear_ratios))  # 84363105
