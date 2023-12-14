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
        # The current damaged group must not skip any damaged springs
        return None

    return group_span

# Testing that the find_next_match regex works as expected

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
        # Failure base case, no damaged groups left for damaged spring leftover
        return 0

    if len(remaining_groups) == 0:
        # Successful base case, matched all groups
        return 1

    current_group = remaining_groups.pop(0)
    group_match = find_next_match(remaining_springs, current_group)
    if group_match is None:
        # Failed to match the group against the remaining springs
        return 0

    possibilities = 0
    more_matches = True
    while more_matches:
        next_remaining_start = group_match[1] + 1
        next_springs = remaining_springs[next_remaining_start:]

        # For each possible arrangement of the current group, we multiply it with
        # the possible arrangements of the remaining groups.
        #
        # A result of 0 indicates an impossible arrangement, and this will propagate
        # recursively back to the first group, invalidating the arrangement.
        possibilities += 1 * count_record_possibilities(Record(next_springs, remaining_groups))

        if remaining_springs[group_match[0]] == '#':
            # No more other positions are possible for the current group since we can't
            # skip damaged springs in the record
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
    for record in records:
        possibilities = count_record_possibilities(record)
        if unfold:
            possibilities = count_record_possibilities(unfold_record(record, 2))
            possibilities = count_record_possibilities(unfold_record(record, 3))
            possibilities = count_record_possibilities(unfold_record(record, 4))
            possibilities = count_record_possibilities(unfold_record(record, 5))
        valid_arrangements += possibilities
    return valid_arrangements

print('Part 1: ', count_valid_arrangements(records, unfold=False)) # 7118
print('Part 2: ', count_valid_arrangements(records, unfold=True))  # 7030194981795
