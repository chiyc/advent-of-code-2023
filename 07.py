from collections import namedtuple
from input import read_input


Hand = namedtuple('Hand', ['cards', 'bid'])

hands = []
for _hand in read_input(7):
    _cards, _bid = _hand.split(' ')
    hands.append(Hand(list(_cards), int(_bid)))

def count_cards(cards):
    count = {}
    for card in cards:
        if card not in count:
            count[card] = 0
        count[card] += 1
    return count

def get_hand_type_key(card_count):
    # 50000 five of a kind
    # 41000 four of a kind
    # 32000 full house
    # 31100 three of a kind
    # 22100 two pair
    # 21110 one pair
    # 11111 high card
    counts = sorted(card_count.values(), reverse=True)
    hand_type_key = ''.join(str(c) for c in counts).ljust(5, '0')
    return hand_type_key

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
# rank starts at 1 with weakest
CARD_RANK = {
    card: i + 1 for i, card in enumerate(CARDS)
}

CARDS_WITH_JOKERS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
CARD_RANK_WITH_JOKERS = {
    card: i + 1 for i, card in enumerate(CARDS_WITH_JOKERS)
}

def get_hand_cards_key(cards, card_rank):
    # transforms cards into padded numbers, weakest card starting at 1
    return ''.join(map(lambda c: str(card_rank[c]).rjust(2, '0'), cards))

def play_jokers(num_jokers, hand_type_key):
    # maps the number of jokers and current hand into a possible better hand
    joker_strategy = {
        5: {}, # already have the best hand
        4: {
            "41000": "50000" # 4 jokers can act as the other card
        },
        3: {
            "32000": "50000",
            "31100": "41000",
        },
        2: {
            "32000": "50000",
            "22100": "41000",
            "21110": "31100",
        },
        1: {
            "41000": "50000",
            "31100": "41000",
            "22100": "32000",
            "21110": "31100",
            "11111": "21110",
        },
        0: {}, # can't do anything with 0 jokers
    }
    return joker_strategy[num_jokers].get(hand_type_key, hand_type_key)

def hand_strength(hand, j_as_joker=False):
    card_count = count_cards(hand.cards)
    hand_type_key = get_hand_type_key(card_count)
    if j_as_joker:
        hand_type_key = play_jokers(card_count.get('J', 0), hand_type_key)

    card_rank = CARD_RANK_WITH_JOKERS if j_as_joker else CARD_RANK
    cards_key = get_hand_cards_key(hand.cards, card_rank)

    return hand_type_key + cards_key

def calculate_winnings(hands, j_as_joker=False):
    sorted_hands = sorted(hands, key=lambda h: hand_strength(h, j_as_joker))
    winnings = sum([hand.bid * (i + 1) for i, hand in enumerate(sorted_hands)])
    return winnings

print('Part 1: ', calculate_winnings(hands, j_as_joker=False)) # 251287184
print('Part 2: ', calculate_winnings(hands, j_as_joker=True))  # 250757288
