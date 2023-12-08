from math import lcm, prod
from input import read_input


puzzle_input = read_input(8)
instructions = list(next(puzzle_input))
next(puzzle_input)

network = {}
for _line in puzzle_input:
    tail, _heads = _line.split(' = ')
    left, right = _heads[1:-1].split(', ')
    network[tail] = {
        'L': left,
        'R': right,
    }

def follow_instructions(network, instructions, starting_node, is_end):
    num_instructions = len(instructions)
    steps = 0
    current_node = starting_node
    while not is_end(current_node):
        instruction = instructions[steps % num_instructions]
        next_node = network[current_node][instruction]
        steps += 1
        current_node = next_node
    return steps

def follow_instructions_as_ghost(network, instructions):
    starting_nodes = [n for n in network.keys() if n[-1] == 'A']
    steps_to_end = [
        follow_instructions(network, instructions, n, lambda n: n[-1] == 'Z')
        for n in starting_nodes
    ]
    return lcm(*steps_to_end)

print('Part 1: ', follow_instructions(network, instructions, 'AAA', lambda n: n == 'ZZZ')) # 11911
print('Part 2: ', follow_instructions_as_ghost(network, instructions)) # 10151663816849
