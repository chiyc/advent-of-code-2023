from input import read_input


mirrors = []
mirror = []
for i, row in enumerate(read_input(13)):
    if row == "": # End of this mirror
        mirrors.append(mirror)
        mirror = []
    else:
        mirror.append(list(row))
mirrors.append(mirror) # Get the last mirror

def check_vertical_reflection(mirror, mirror_col):
    assert 1 <= mirror_col < len(mirror[0])
    for row in mirror:
        for j in range(mirror_col):
            jr = mirror_col + (mirror_col - j - 1)
            if jr < len(row) and row[j] != row[jr]:
                return False
    return True

def check_horizontal_reflection(mirror, mirror_row):
    assert 1 <= mirror_row < len(mirror)
    for j in range(len(mirror[0])):
        col = ''.join([mirror[i][j] for i, _ in enumerate(mirror)])
        for i in range(mirror_row):
            ir = mirror_row + (mirror_row - i - 1)
            if ir < len(mirror) and col[i] != col[ir]:
                return False
    return True

def find_mirror_position(mirror):
    for i in range(1, len(mirror)):
        if check_horizontal_reflection(mirror, i):
            return (i, 0)

    for j in range(1, len(mirror[0])):
        if check_vertical_reflection(mirror, j):
            return (0, j)

    return (0, 0)

def find_mirror_positions(mirror):
    positions = []
    for i in range(1, len(mirror)):
        if check_horizontal_reflection(mirror, i):
            positions.append((i, 0))

    for j in range(1, len(mirror[0])):
        if check_vertical_reflection(mirror, j):
            positions.append((0, j))

    return positions

def find_smudged_mirror_position(mirror, index):
    original_mirror_location = find_mirror_position(mirror)
    for i, row in enumerate(mirror):
        for j, _ in enumerate(row):
            original_symbol = mirror[i][j]
            new_symbol = {'#': '.', '.': '#'}[original_symbol]
            mirror[i][j] = new_symbol

            new_mirror_positions = find_mirror_positions(mirror)
            if original_mirror_location in new_mirror_positions:
                new_mirror_positions.remove(original_mirror_location)

            if len(new_mirror_positions) > 0:
                return new_mirror_positions[0]
            else:
                mirror[i][j] = original_symbol
    assert False

def summarize_mirror_positions(mirrors, smudge=False):
    solution = 0
    row, col = 0, 1
    for i, mirror in enumerate(mirrors):
        position = (
            find_smudged_mirror_position(mirror, i)
            if smudge else find_mirror_position(mirror)
        )
        solution += position[col] + 100 * position[row]
    return solution

print('Part 1: ', summarize_mirror_positions(mirrors)) # 36015
print('Part 2: ', summarize_mirror_positions(mirrors, smudge=True)) # 35335
