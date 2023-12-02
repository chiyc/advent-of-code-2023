from input import read_input





def parse_game(game_line):
    game_name, game_rounds = game_line.split(': ')
    game_id = game_name.split(' ')[1]

    game = []
    for _round in game_rounds.split('; '):
        round = {}
        for _cubes in _round.split(', '):
            count, cube = _cubes.split(' ')
            round[cube] = int(count)
        game.append(round)
    return int(game_id), game


BAG = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def possible_round(round):
    if sum(round.values()) > sum(BAG.values()):
        return False

    for color, count in round.items():
        if count > BAG[color]:
            return False

    return True


def possible_game(game):
    rounds = game[1]
    return all(map(lambda r: possible_round(r), rounds))


def required_cubes(game):
    max_seen = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    rounds = game[1]
    for round in rounds:
        for color, count in round.items():
            max_seen[color] = max(count, max_seen[color])

    return max_seen

def cube_set_power(cube_set):
    return cube_set['red'] * cube_set['green'] * cube_set['blue']


possible_games = []
cube_set_powers = []
for line in read_input(2):
    game = parse_game(line)

    if possible_game(game):
        possible_games.append(game[0])

    power = cube_set_power(required_cubes(game))
    cube_set_powers.append(power)

print(f'Part 1: ', sum(possible_games))  # 3099
print(f'Part 2: ', sum(cube_set_powers)) # 72970
