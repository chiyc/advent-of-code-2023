from input import read_input


platform = []
for row in read_input(14):
    platform.append(list(row))

def tilt_north_or_south(platform, north=True):
    cols = []
    for j, _ in enumerate(platform[0]):
        col = ''.join([platform[i][j] for i, _ in enumerate(platform)])
        col_sections = col.split('#')
        col = []
        for section in col_sections:
            tilted_section = ''.join(sorted(section, reverse=north))
            col.append(tilted_section)
        cols.append('#'.join(col))

    tilted_platform = []
    for i, _ in enumerate(cols[0]):
        row = [cols[j][i] for j, _ in enumerate(cols)]
        tilted_platform.append(row)
    return tilted_platform

def tilt_west_or_east(platform, west=True):
    tilted_platform = []
    for row in platform:
        row_sections = ''.join(row).split('#')
        row = []
        for section in row_sections:
            tilted_section = ''.join(sorted(section, reverse=west))
            row.append(tilted_section)
        tilted_platform.append(list('#'.join(row)))
    return tilted_platform

def cycle_platform(platform):
    tilted_north = tilt_north_or_south(platform, north=True)
    tilted_west = tilt_west_or_east(tilted_north, west=True)
    tilted_south = tilt_north_or_south(tilted_west, north=False)
    tilted_east = tilt_west_or_east(tilted_south, west=False)
    return tilted_east

def calculate_load(platform):
    length = len(platform)
    load = 0
    for i, row in enumerate(platform):
        for j, tile in enumerate(row):
            if tile == 'O':
                load += length - i
    return load

def print_platform(platform):
    for row in platform:
        print(''.join(row))

print('Part 1: ', calculate_load(tilt_north_or_south(platform, north=True))) # 110677

# In Part 2, we need to find how the load values repeat to extrapolate the
# pattern to 1 billion cycles

# Possible dynamic programming solution?
# Need to somehow compare the longest repeated sequence seen so far
# Two pointers?

# cycled_platform = platform
# cycled_loads = []
# repeating_cycles = []
# for j in range(300):
#     cycled_platform = cycle_platform(cycled_platform)
#     load = calculate_load(cycled_platform)
#     cycled_loads.append(load)
#     repeating_cycles.append([0])
#     if j > 0:
#         for i in range(j+1):

# Working it out by manually observing and narrowing the behavior instead

load_cycles = {}
cycled_platform = platform
for i in range(1_000_000_000):
    cycled_platform = cycle_platform(cycled_platform)
    load = calculate_load(cycled_platform)

    if load not in load_cycles:
        load_cycles[load] = []

    elif len(load_cycles[load]) == 5:
        # Looks like cycle loads repeat themselves roughly by this point
        if (load_cycles[load][4] - load_cycles[load][3] == load_cycles[load][3] - load_cycles[load][2]):
            repeating_load_cycles = {load: cycles for load, cycles in load_cycles.items() if len(cycles) > 3}

            cycle_start = min(cycles[0] for cycles in repeating_load_cycles.values())
            cycle_end = max(cycles[0] for cycles in repeating_load_cycles.values())

            cycle_length = cycle_end - cycle_start + 1
            cycles_until_last = 1_000_000_000 - cycle_start
            relative_repeated_position = cycles_until_last % cycle_length
            repeated_cycle = cycle_start + relative_repeated_position
            print('Part 2: ', [load for load, cycles in repeating_load_cycles.items() if repeated_cycle in cycles][0]) # 90551
            break

    cycle = i+1
    load_cycles[load].append(cycle)
