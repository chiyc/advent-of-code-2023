from input import read_input


num_digits = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9',
]
str_digits = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
]

def parse_digits(line, include_words):
    digits = []

    i = 0
    while i < len(line):
        if line[i] in num_digits:
            digits.append(line[i])

        elif include_words:
            for d, word in enumerate(str_digits):
                if line[i:i+len(word)] == word:
                    digits.append(num_digits[d])
                    i += len(word) - 2 # backtrack 2 to offset the +1 below
                    break
        i += 1

    return digits


def calibrate(line, include_words):
    digits = parse_digits(line, include_words)
    return int(digits[0]+digits[-1])


calibration_part1 = 0
calibration_part2 = 0
for line in read_input(1):
    calibration_part1 += calibrate(line, include_words=False)
    calibration_part2 += calibrate(line, include_words=True)
print(f'Part 1: {calibration_part1}') # 56397
print(f'Part 2: {calibration_part2}') # 55701
