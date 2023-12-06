import math
import re
from input import read_input


puzzle_input = read_input(6)
times = map(int, re.split(r'\s+', next(puzzle_input).split(':')[1].strip()))
records = map(int, re.split(r'\s+', next(puzzle_input).split(':')[1].strip()))

def get_answer(times, records):
    answer = 1
    for time, record in zip(times, records):
        winning_rounds = 0
        for duration in range(time+1):
            distance = duration * (time - duration)
            if distance > record:
                winning_rounds += 1
        answer *= winning_rounds
    return answer

print('Part 1: ', get_answer(times, records)) # 633080

puzzle_input = read_input(6)
times = int(next(puzzle_input).split(':')[1].replace(' ', ''))
records = int(next(puzzle_input).split(':')[1].replace(' ', ''))

def get_answer_faster(times, records):
    answer = 1
    for t, r in zip(times, records):
        # as a quadratic polynomial, we have the following constants
        a, b, c = -1, t, -r
        d = b * b - 4 * a * c # discriminant
        d_sqrt = math.sqrt(d)

        rhs = d_sqrt / (2 * a)
        lhs = -b / (2 * a)

        lower_bound = math.ceil(lhs + rhs)
        upper_bound = math.floor(lhs - rhs)

        answer *= upper_bound - lower_bound + 1
    return answer

print('Part 2: ', get_answer_faster([times], [records])) # 20048741
