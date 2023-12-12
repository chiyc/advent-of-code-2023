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
    piece_map = {0: '.', 1: '#'}
    for n in range(2 ** missing_count):
        possibility = ''
        for _i in range(0, missing_count):
            i = 2 ** _i
            piece = piece_map[(n // i) % 2]
            possibility += piece
        yield possibility

def generate_record_possibilities(record):
    springs, damaged_groups = record
    total_damaged_springs = sum(damaged_groups)

    missing = springs.count('?')
    for replacement in generate_replacement_possibilities(missing):
        record_possibility = springs
        for piece in replacement:
            record_possibility = record_possibility.replace('?', piece, 1)
        if record_possibility.count('#') == total_damaged_springs:
            yield Record(record_possibility, record.damaged_groups)

def unfold_record(record):
    springs, damaged_groups = record
    unfolded_springs = '?'.join([springs] * 5)
    unfolded_groups = damaged_groups * 5
    return Record(unfolded_springs, unfolded_groups)

def count_valid_arrangements(records, unfold=False):
    valid_arrangements = 0
    for i, record in enumerate(records):
        if unfold:
            record = unfold_record(record)
        for possibility in generate_record_possibilities(record):
            if is_valid_record(possibility):
                valid_arrangements += 1
        # print(f'Record {i}: {valid_arrangements} cumulative valid arrangements')
    return valid_arrangements

print('Part 1: ', count_valid_arrangements(records, unfold=False)) # 7118
print('Part 2: ', count_valid_arrangements(records, unfold=True)) #
