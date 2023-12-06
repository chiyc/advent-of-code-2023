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
            velocity = duration
            remaining_time = time - duration
            distance = velocity * remaining_time
            if distance > record:
                winning_rounds += 1
        answer *= winning_rounds
    return answer

print('Part 1: ', get_answer(times, records)) # 633080

puzzle_input = read_input(6)
times = int(next(puzzle_input).split(':')[1].replace(' ', ''))
records = int(next(puzzle_input).split(':')[1].replace(' ', ''))

print('Part 2: ', get_answer([times], [records])) # 20048741
