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

def find_nth_cycle_load(platform, total_cycles):
    platform_cycles = [None] # Pad to 1-index cycles
    platform_cycles_map = {}

    cycled_platform = platform
    for i in range(total_cycles):
        cycle = i + 1

        cycled_platform = cycle_platform(cycled_platform)
        platform_key = ''.join([''.join(row) for row in cycled_platform])

        if platform_key in platform_cycles_map:
            first_seen_cycle = platform_cycles_map[platform_key]
            cycle_length = cycle - first_seen_cycle
            cycles_until_last = total_cycles - first_seen_cycle
            relative_repeated_position = cycles_until_last % cycle_length
            repeated_cycle = first_seen_cycle + relative_repeated_position
            return calculate_load(platform_cycles[repeated_cycle])

        else:
            platform_cycles.append(cycled_platform)
            platform_cycles_map[platform_key] = cycle

print('Part 2: ', find_nth_cycle_load(platform, 1_000_000_000)) # 90551
