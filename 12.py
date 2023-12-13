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

def unfold_record(record, factor):
    springs, damaged_groups = record
    unfolded_springs = '?'.join([springs] * factor)
    unfolded_groups = damaged_groups * factor
    return Record(unfolded_springs, unfolded_groups)

def count_record_possibilities(record):
    total_possibilities = 0
    start_damaged = 0
    end_damaged = 0
    for possibility in generate_record_possibilities(record):
        if is_valid_record(possibility):
            total_possibilities += 1
            if possibility.springs[0] == '#':
                start_damaged += 1
            if possibility.springs[-1] == '#':
                end_damaged += 1
    return total_possibilities, start_damaged, end_damaged

def count_valid_arrangements(records, unfold=False):
    valid_arrangements = 0
    for i, record in enumerate(records):
        possibilities, start_damaged, end_damaged = count_record_possibilities(record)

        if unfold:
            # This approach tries to extrapolate the sum from adding a single '?'
            # It works on the sample input but will undercount certain input
            springs, damaged_groups = record
            start_undamaged = possibilities - start_damaged
            end_undamaged = possibilities - end_damaged

            left_unfold = Record(f'{springs}?', damaged_groups)
            left_possibilities, left_start_damaged, left_end_damaged = count_record_possibilities(left_unfold)
            left_end_undamaged = left_possibilities - left_end_damaged

            right_unfold = Record(f'?{springs}', damaged_groups)
            right_possibilities, right_start_damaged, right_end_damaged = count_record_possibilities(right_unfold)
            right_start_undamaged = right_possibilities - right_start_damaged

            unfolded_possibilities = max(
                start_undamaged * left_possibilities + start_damaged * left_end_undamaged,
                end_undamaged * right_possibilities + end_damaged * right_start_undamaged,
            )
            possibilities = possibilities * (unfolded_possibilities // possibilities) ** 4

            """
            This is another approach that tries to extrapolate the 5x unfold from 2x.
            It's still way too slow coupled with brute forcing the possibilites. And I'm
            not certain it would be correct for certain inputs.

            double_possibilities, _, _ = count_record_possibilities(unfold_record(record, 2))
            possibilities = possibilities * (double_possibilities // possibilities) ** 4

            Record 0: 2592 valid arrangements
            Record 1: 1259712 valid arrangements
            Record 2: 16 valid arrangements
            Record 3: 60000 valid arrangements
            Record 4: 1875 valid arrangements
            Record 5: 65610000 valid arrangements
            Record 6: 32 valid arrangements
            Record 7: 5308416 valid arrangements
            Record 8: 162 valid arrangements
            Record 9: 19683 valid arrangements
            Record 10: 1250 valid arrangements
            Record 11: 18708704 valid arrangements
            Record 12: 768 valid arrangements
            Record 13: 124416 valid arrangements
            Record 14: 24576 valid arrangements
            Record 15: 5859375 valid arrangements
            Record 16: 1250 valid arrangements
            Record 17: 56224830 valid arrangements
            """


        print(f'Record {i}: {possibilities} valid arrangements')
        valid_arrangements += possibilities
    return valid_arrangements

print('Part 1: ', count_valid_arrangements(records, unfold=False)) # 7118

sample_records = [                          #                        L  R    x2
    Record('?.??#?', [1, 2]),               #     12 from 3       -  5, 4    12    12 // 3 ==  4
    Record('???.###', [1,1,3]),             #      1 from 1       -  1, 1     1    1 //  1 ==  1
    Record('.??..??...?##.', [1,1,3]),      #  16384 from 4       -  8, 4    32   32 //  4 ==  8
    Record('?#?#?#?#?#?#?#?', [1,3,1,6]),   #      1 from 1       -  1, 1     1    1 //  1 ==  1
    Record('????.#...#...', [4,1,1]),       #     16 from 1       -  2, 1     2    2 //  1 ==  2
    Record('????.######..#####.', [1,6,5]), #   2500 from 4       -  5, 4    20   20 //  4 ==  5
    Record('?###????????', [3,2,1]),        # 506250 from 10      - 10, 15  150  150 // 10 == 15
]

""" unfold left              unfold right
       ?.??#??     ?.??#?   ??.??#?            ?.??#???.??#?
                                                   # ## # ##  <-- How to catch this case??
       #..##..     #..##.   #...##.            #..##.#...##.      Not possible with current approach
                                               #..##.#....##
       #...##.     #...##   .#..##.            #..##..#..##.
       ..#.##.     ..#.##   #....##            #..##..#...##
                            .#...##            #..##....#.##
                            ...#.##            #...##.#..##.
                                               #...##.#...##
                                               #...##...#.##
                                               ..#.##.#..##.
                                               ..#.##.#...##
                                               ..#.##...#.##
"""

print('Part 2: ', count_valid_arrangements(sample_records, unfold=True)) # 316598322037 is too low
