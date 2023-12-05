from collections import namedtuple
from input import read_input


Map = namedtuple('Map', ['ds', 'ss', 'l'])
Range = namedtuple('Range', ['start', 'end']) # inclusive end

puzzle_input = read_input(5)

seeds = []
_seeds = next(puzzle_input)
seeds = list(map(int, _seeds.split(': ')[1].split(' ')))

def get_map(map_name, puzzle_input):
    result = []

    while not next(puzzle_input).startswith(map_name):
        pass

    next_map = next(puzzle_input)
    while next_map != '':
        ds, ss, l = map(int, next_map.split(' '))
        result.append(Map(ds, ss, l))
        try:
            next_map = next(puzzle_input)
        except StopIteration:
            next_map = ''

    return sorted(result, key=lambda item: item.ss)

seed_to_soil = get_map('seed-to-soil', puzzle_input)
soil_to_fertilizer = get_map('soil-to-fertilizer', puzzle_input)
fertilizer_to_water = get_map('fertilizer-to-water', puzzle_input)
water_to_light = get_map('water-to-light', puzzle_input)
light_to_temperature = get_map('light-to-temperature', puzzle_input)
temperature_to_humidity = get_map('temperature-to-humidity', puzzle_input)
humidity_to_location = get_map('humidity-to-location', puzzle_input)

resource_maps = {
    'seed-to-soil': seed_to_soil,
    'soil-to-fertilizer': soil_to_fertilizer,
    'fertilizer-to-water': fertilizer_to_water,
    'water-to-light': water_to_light,
    'light-to-temperature': light_to_temperature,
    'temperature-to-humidity': temperature_to_humidity,
    'humidity-to-location': humidity_to_location,
}

# Part 1

def map_id(id, map_piece):
    return map_piece.ds + (id - map_piece.ss)

def map_resource(id, resource_map):
    for _map in resource_map:
        if _map.ss <= id < _map.ss + _map.l:
            return map_id(id, _map)
    return id

def map_seed_to_location(seed_id, resource_maps):
    soil_id = map_resource(seed_id, resource_maps['seed-to-soil'])
    fertilizer_id = map_resource(soil_id, resource_maps['soil-to-fertilizer'])
    water_id = map_resource(fertilizer_id, resource_maps['fertilizer-to-water'])
    light_id = map_resource(water_id, resource_maps['water-to-light'])
    temperature_id = map_resource(light_id, resource_maps['light-to-temperature'])
    humidity_id = map_resource(temperature_id, resource_maps['temperature-to-humidity'])
    location_id = map_resource(humidity_id, resource_maps['humidity-to-location'])
    return location_id


seed_locations = [map_seed_to_location(seed, resource_maps) for seed in seeds]
print('Part 1: ', min(seed_locations)) # 178159714

# Part 2

# We're now dealing with a range of values. For each resource map, a single range of
# values can now be mapped into multiple ranges that are divided by the boundaries

# Sorting everything, which I've added to Part 1 above, will help simplify the logic.

def map_resource_range(input_range, resource_map):
    output_ranges = []
    start, end = input_range

    # just used for basic assertion over output
    input_values = end - start + 1

    # resource_map is ordered by source range start
    for _map in resource_map:
        s_start, s_end = _map.ss, _map.ss + _map.l - 1 # inclusive interval

        # inner overlap
        if s_start <= start <= s_end and s_start <= end <= s_end:
            output_ranges.append(Range(map_id(start, _map), map_id(end, _map)))
            end = start - 1 # this 'kills' the range by making it a negative length interval
            break

        # overlap on left
        elif s_start <= end <= s_end and start < s_start:
            output_ranges.append(Range(map_id(s_start, _map), map_id(end, _map)))
            end = s_start - 1

            # remaining non-overlapping range on the left side is guaranteed to
            # not fit into any other functions due to sorting
            output_ranges.append(Range(start, end))
            end = start - 1
            break

        # overlap on right
        elif s_start <= start <= s_end and s_end < end:
            output_ranges.append(Range(map_id(start, _map), map_id(s_end, _map)))
            start = s_end + 1

        # complete outer overlap
        elif start < s_start and s_end < end:
            output_ranges.append(Range(map_id(s_start, _map), map_id(s_end, _map)))
            output_ranges.append(Range(start, s_start - 1))
            start = s_end + 1

        # no overlap
        else:
            pass

    # portion of the input_range still remaining
    if start <= end:
        output_ranges.append(Range(start, end))

    # asserts that the output ranges contain the same amount of numbers
    output_values = 0
    for r in output_ranges:
        output_values += r.end - r.start + 1
    assert input_values == output_values

    return output_ranges

def map_resource_ranges(input_ranges, resource_map):
    output_ranges = []
    for input_range in input_ranges:
        output_ranges += map_resource_range(input_range, resource_map)
    return output_ranges

def map_seed_ranges_to_location_ranges(seed_ranges, resource_maps):
    soil_ranges = map_resource_ranges(seed_ranges, resource_maps['seed-to-soil'])
    fertilizer_ranges = map_resource_ranges(soil_ranges, resource_maps['soil-to-fertilizer'])
    water_ranges = map_resource_ranges(fertilizer_ranges, resource_maps['fertilizer-to-water'])
    light_ranges = map_resource_ranges(water_ranges, resource_maps['water-to-light'])
    temperature_ranges = map_resource_ranges(light_ranges, resource_maps['light-to-temperature'])
    humidity_ranges = map_resource_ranges(temperature_ranges, resource_maps['temperature-to-humidity'])
    location_ranges = map_resource_ranges(humidity_ranges, resource_maps['humidity-to-location'])
    return location_ranges


seed_ranges = []
for i in range(0, len(seeds), 2):
    seed_ranges.append(Range(seeds[i], seeds[i] + seeds[i+1] - 1))
seed_ranges = sorted(seed_ranges, key=lambda item: item.start)

location_ranges = map_seed_ranges_to_location_ranges(seed_ranges, resource_maps)

print('Part 2: ', min(location_ranges, key=lambda r: r.start).start) # 100165128
