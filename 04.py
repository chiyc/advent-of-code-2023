import re
from input import read_input

def parse_card_numbers(line):
    _numbers = line.split(': ')[1].strip()
    _my_numbers, _winning = re.split(r'\s+\|\s+', _numbers)
    return set(re.split(r'\s+', _my_numbers)), set(re.split(r'\s+', _winning))

def num_matching(card):
    my_numbers, winning = card
    my_winning_numbers = winning.intersection(my_numbers)
    return len(my_winning_numbers)

def calculate_points(card):
    winners = num_matching(card)
    return 2 ** (winners - 1) if winners > 0 else 0

def total_points(cards):
    points = []
    for card in cards:
        points.append(calculate_points(card))
    return sum(points)

def total_scratchcards(cards):
    card_counts = {i: 1 for i in range(1, len(cards) + 1)}

    for i, card in enumerate(cards):
        card_id = i + 1
        card_count = card_counts[card_id]

        winners = num_matching(card)
        next_card = card_id + 1
        for won in range(next_card, next_card + winners):
            card_counts[won] += card_count

    return sum(card_counts.values())

cards = []
for _line in read_input(4):
    cards.append(parse_card_numbers(_line))

print('Part 1: ', total_points(cards)) # 23235
print('Part 2: ', total_scratchcards(cards)) # 5920640