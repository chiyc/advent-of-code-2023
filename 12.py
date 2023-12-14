import re
from collections import namedtuple
from input import read_input


Record = namedtuple('Record', ['springs', 'damaged_groups'])

records = []
for _line in read_input(12):
    springs, _damaged_groups = _line.split(' ')
    damaged_groups = [int(n) for n in _damaged_groups.split(',')]
    records.append(Record(springs, damaged_groups))

def unfold_record(record, factor):
    springs, damaged_groups = record
    unfolded_springs = '?'.join([springs] * factor)
    unfolded_groups = damaged_groups * factor
    return Record(unfolded_springs, unfolded_groups)

def find_next_match(remaining_springs, damaged_group):
    pattern = re.compile(f'(?<!#)([#\?]{{{damaged_group}}})(?!#)')
    group_match = pattern.search(remaining_springs)
    if group_match is None:
        return None

    group_span = group_match.span(1)
    if '#' in remaining_springs[0:group_span[0]]:
        return None

    return group_span

assert find_next_match('###', 3) == (0, 3)
assert find_next_match('???', 3) == (0, 3)
assert find_next_match('??#', 3) == (0, 3)
assert find_next_match('#??', 3) == (0, 3)
assert find_next_match('?##', 3) == (0, 3)
assert find_next_match('#?#', 3) == (0, 3)
assert find_next_match('##?', 3) == (0, 3)

assert find_next_match('#?#?', 3) == (0, 3)
assert find_next_match('?#?#', 3) == (1, 4)
assert find_next_match('##??', 3) == (0, 3)
assert find_next_match('??##', 3) == (1, 4)
assert find_next_match('?##?', 3) == (0, 3)

assert not find_next_match('##?#', 3)
assert not find_next_match('#?##', 3)
assert not find_next_match('#??#', 3)

memo = {}
def count_record_possibilities(record):
    memo_record = Record(record.springs, tuple(record.damaged_groups))
    if memo_record in memo:
        return memo[memo_record]
    remaining_springs, damaged_groups = record

    remaining_groups = damaged_groups.copy()
    if len(remaining_groups) == 0 and '#' in remaining_springs:
        return 0
    elif len(remaining_groups) == 0:
        return 1

    current_group = remaining_groups.pop(0)
    group_match = find_next_match(remaining_springs, current_group)
    if group_match is None:
        return 0

    possibilities = 0
    more_matches = True
    while more_matches:
        next_remaining_start = group_match[1] + 1
        next_springs = remaining_springs[next_remaining_start:]
        possibilities += 1 * count_record_possibilities(Record(next_springs, remaining_groups))

        if remaining_springs[group_match[0]] == '#':
            more_matches = False
        else:
            remaining_springs = remaining_springs[group_match[0]+1:]
            group_match = find_next_match(remaining_springs, current_group)
            if group_match is None:
                more_matches = False
    memo[memo_record] = possibilities
    return possibilities

def count_valid_arrangements(records, unfold=False):
    valid_arrangements = 0
    for i, record in enumerate(records):
        possibilities = count_record_possibilities(record)
        # print(f'Record {i}: {record.springs} - {record.damaged_groups} - {possibilities} arrangements')
        if unfold:
            possibilities = count_record_possibilities(unfold_record(record, 1))
            possibilities = count_record_possibilities(unfold_record(record, 2))
            possibilities = count_record_possibilities(unfold_record(record, 3))
            possibilities = count_record_possibilities(unfold_record(record, 4))
            possibilities = count_record_possibilities(unfold_record(record, 5))
        valid_arrangements += possibilities
    return valid_arrangements

sample_records = [                          #                        L  R    x2
    # Record('?.??#?', [1, 2]),               #     12 from 3       -  5, 4    12    12 // 3 ==  4    new approach 5
    Record('???.###', [1,1,3]),             #      1 from 1       -  1, 1     1    1 //  1 ==  1    new approach 1
    Record('.??..??...?##.', [1,1,3]),      #  16384 from 4       -  8, 4    32   32 //  4 ==  8    new approach 41
    Record('?#?#?#?#?#?#?#?', [1,3,1,6]),   #      1 from 1       -  1, 1     1    1 //  1 ==  1    new approach 1
    Record('????.#...#...', [4,1,1]),       #     16 from 1       -  2, 1     2    2 //  1 ==  2    new approach 1
    Record('????.######..#####.', [1,6,5]), #   2500 from 4       -  5, 4    20   20 //  4 ==  5    new approach 4
    Record('?###????????', [3,2,1]),        # 506250 from 10      - 10, 15  150  150 // 10 == 15    new approach 10
] # 24 total for part 1

print('Part 1: ', count_valid_arrangements(records, unfold=False)) # 7118
print('Part 2: ', count_valid_arrangements(records, unfold=True))  # 7030194981795
