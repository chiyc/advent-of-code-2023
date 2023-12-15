import re
from collections import namedtuple
from functools import reduce
from input import read_input


steps = next(read_input(15)).split(',')

def holiday_hash(step):
    result = 0
    for c in step:
        result += ord(c)
        result *= 17
        result %= 256
    return result

verification_number = reduce(lambda total, step: total + holiday_hash(step), steps, 0)
print('Part 1: ', verification_number) # 510013

Lens = namedtuple('Lens', ['label', 'focal'])

def parse_step(step):
    label, focal_length = re.split(r'[=-]', step)
    return label, re.search(r'[=-]', step).group(0), int(focal_length or 0)

def print_boxes(boxes):
    for box, lenses in boxes.items():
        if lenses:
            print(f'Box {box}: ', lenses)
    print('\n')

def arrange_lenses(steps):
    boxes = {i: [] for i in range(256)}
    for step in steps:
        label, operation, focal_length = parse_step(step)
        box = holiday_hash(label)

        lens_with_label_index = None
        for i, lens in enumerate(boxes[box]):
            if lens.label == label:
                lens_with_label_index = i
                break

        if operation == '-':
            if lens_with_label_index is not None:
                boxes[box].pop(lens_with_label_index)

        elif operation == '=':
            if lens_with_label_index is not None:
                boxes[box][lens_with_label_index] = Lens(label, focal_length)
            else:
                boxes[box].append(Lens(label, focal_length))
        # print_boxes(boxes)
    return boxes

def get_total_focusing_power(boxes):
    focusing_power = 0
    for box, lenses in enumerate(boxes.values()):
        for i, lens in enumerate(lenses):
            focusing_power += (box + 1) * (i + 1) * lens.focal
    return focusing_power

focusing_power = get_total_focusing_power(arrange_lenses(steps))
print('Part 2: ', focusing_power) # 268497
