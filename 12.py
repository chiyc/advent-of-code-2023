import re
from collections import namedtuple
from input import read_input


Record = namedtuple('Record', ['springs', 'damaged_groups'])

records = []
for _line in read_input(12):
    springs, _damaged_groups = _line.split(' ')
    damaged_groups = [int(n) for n in _damaged_groups.split(',')]
    records.append(Record(springs, damaged_groups))

def is_valid_record(record):
    springs, damaged_groups = record
    assert springs.count('?') == 0
    assert springs.count('#') == sum(damaged_groups)

    damaged_groups_raw_regex = '\.+'.join([
        f'#{{{group}}}'
        for group in damaged_groups
    ])
    pattern = re.compile(f'\.*{damaged_groups_raw_regex}\.*')
    return pattern.match(springs)


def generate_replacement_possibilities(missing_count):
    possibilities = [''] * 2 ** missing_count
    piece_map = {0: '.', 1: '#'}
    for _i in range(0, missing_count):
        i = 2 ** _i
        for n, _ in enumerate(possibilities):
            piece = piece_map[(n // i) % 2]
            possibilities[n] += piece
    return possibilities

def generate_record_possibilities(record):
    record_possibilities = []

    springs, damaged_groups = record
    total_damaged_springs = sum(damaged_groups)

    missing = springs.count('?')
    replacements = generate_replacement_possibilities(missing)

    for replacement in replacements:
        record_possibility = springs

        for piece in replacement:
            record_possibility = record_possibility.replace('?', piece, 1)

        if record_possibility.count('#') == total_damaged_springs:
            record_possibilities.append(Record(record_possibility, record.damaged_groups))

    return record_possibilities

def count_valid_arrangements(records):
    valid_arrangements = 0
    for record in records:
        possibilities = generate_record_possibilities(record)
        for possibility in possibilities:
            if is_valid_record(possibility):
                valid_arrangements += 1
    return valid_arrangements

print('Part 1: ', count_valid_arrangements(records)) # 7118
