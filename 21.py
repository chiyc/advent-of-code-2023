from collections import deque, namedtuple
from input import read_input


grid = []
for row in read_input(21):
    grid.append(list(row))

def find_starting_point(grid):
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == 'S':
                return (i, j)
    assert False

Path = namedtuple('Path', ['position', 'steps'])

def step_to_garden(grid, exact_steps=64, infinite=False):
    rows = len(grid)
    cols = len(grid[0])

    grid_steps = {}
    start = find_starting_point(grid)
    next = deque([Path(start, 0)])
    while next:
        position, steps = next.popleft()
        i, j = position

        if steps > exact_steps:
            continue

        if not infinite and (i < 0 or i >= rows or j < 0 or j >= cols):
            continue

        if position in grid_steps:
            continue

        if i < 0 or i >= rows or j < 0 or j >= cols:
            infinite_i = i % rows
            infinite_j = j % rows
            tile = grid[infinite_i][infinite_j]
        else:
            tile = grid[i][j]

        if tile == '#':
            continue

        grid_steps[position] = steps

        next.extend([
            Path((i, j-1), steps + 1),
            Path((i, j+1), steps + 1),
            Path((i-1, j), steps + 1),
            Path((i+1, j), steps + 1),
        ])

    reached_garden_count = 0
    for position, steps in grid_steps.items():
        # Which garden steps are reachable at the exact number of steps with
        # backtracking depends on whether we have an odd or even number of steps
        if steps % 2 == exact_steps % 2:
            reached_garden_count += 1
    return reached_garden_count

print('Part 1: ', step_to_garden(grid, exact_steps=64)) # 3847


"""
This Part 2 solution makes certain assumptions about the input that do not
apply to the example input. The solve_part_2 function will therefore be
incorrect for the example and possibly other puzzle inputs.

The general approach is to use these assumptions to extrapolate the garden plots
reached as we infinitely tile the grid.

1. Completely clear vertical and horizontal lines from the starting point
2. Input grid has relatively few rocks, making all garden tiles reachable in checkerboard pattern
3. The number of steps taken is large enough to reach several grids away
4. Starting point is exactly in the center of a square grid with odd side lengths
"""
def solve_part_2(grid, exact_steps=26501365):
    rows = len(grid)
    cols = len(grid[0])

    initial_starting_point = find_starting_point(grid)
    start_i, start_j = initial_starting_point

    # We'll later count reached garden plots from different points of the grid
    # to understand how the infinite tiling affects the periphery garden plots
    def set_starting_point(grid, point):
        i, j = find_starting_point(grid)
        grid[i][j] = '.'
        i, j = point
        grid[i][j] = 'S'

    # Taking an odd or even number of steps will affect which garden plots
    # are reached in the origin grid and neighboring ones. For grids that
    # are completely covered by the number of steps, tiled neighboring grids
    # will alternative between those reached by an odd or even number of steps
    odd_steps = exact_steps % 2 == 1

    # This sum just ensures we can cover the entire grid from the starting point
    even_step_coverage = exact_steps + 1 if odd_steps else exact_steps
    even_steps_reached = step_to_garden(grid, even_step_coverage)

    # Also determine the reachable garden plots with an odd number of steps
    odd_step_coverage = exact_steps if odd_steps else exact_steps + 1
    odd_steps_reached = step_to_garden(grid, odd_step_coverage)

    total_reached = 0
    origin_grid_reached = odd_steps_reached if odd_steps else even_steps_reached
    alternate_grid_reached =  even_steps_reached if odd_steps else odd_steps_reached
    total_reached += origin_grid_reached

    # Determine how many grids we reach along an axis in one direction (excluding the origin)
    full_axes_grids = (start_j + exact_steps) // cols - 1
    has_second_partial_end = ((start_j + exact_steps) % cols) < (cols // 2 - 1)
    if has_second_partial_end:
        full_axes_grids -= 1

    # Add the garden plots reached by the full grids
    full_axes_grids_reached = (full_axes_grids // 2) * (odd_steps_reached + even_steps_reached)
    if full_axes_grids % 2 == 1:
        full_axes_grids_reached += alternate_grid_reached
    total_reached += 4 * full_axes_grids_reached

    # Now add the garden plots reached by the partially covered grids at each end

    # East end
    east_col = (start_j + exact_steps) % cols
    steps_from_edge = east_col
    set_starting_point(grid, (start_i, 0)) # from left edge
    total_reached += step_to_garden(grid, steps_from_edge)
    if has_second_partial_end:
        total_reached += step_to_garden(grid, cols + steps_from_edge)

    # West end
    set_starting_point(grid, (start_i, cols - 1)) # from east edge
    total_reached += step_to_garden(grid, steps_from_edge)
    if has_second_partial_end:
        total_reached += step_to_garden(grid, cols + steps_from_edge)

    # North end
    set_starting_point(grid, (rows - 1, start_j)) # from south edge
    total_reached += step_to_garden(grid, steps_from_edge)
    if has_second_partial_end:
        total_reached += step_to_garden(grid, rows + steps_from_edge)

    # South end
    set_starting_point(grid, (0, start_j)) # from north edge
    total_reached += step_to_garden(grid, steps_from_edge)
    if has_second_partial_end:
        total_reached += step_to_garden(grid, rows + steps_from_edge)

    # Determine how many are reached by full grids in each quadrant
    full_quadrant_grids_reached = 0
    quadrant_row_grids = full_axes_grids - 1
    quadrant_row = 1
    while quadrant_row_grids > 0:
        odd_row = quadrant_row % 2 == 1
        odd_grids = quadrant_row_grids % 2 == 1
        full_quadrant_grids_reached += (quadrant_row_grids // 2) * (odd_steps_reached + even_steps_reached)
        if odd_grids:
            full_quadrant_grids_reached += origin_grid_reached if odd_row else alternate_grid_reached
        quadrant_row_grids -= 1
        quadrant_row += 1
    total_reached += 4 * full_quadrant_grids_reached

    # Now determine how the partially covered diagonals add to the total reached garden plots.
    # The diagonally covered periphery grids in each quadrant repeat the reached garden plots in twos

    # We use these step calculations for all quadrants since we assume we start in the center
    steps_to_corner = start_j + 1
    remaining_steps_from_corner = (
        steps_from_edge + cols - steps_to_corner
        if has_second_partial_end
        else steps_from_edge - steps_to_corner
    )

    set_starting_point(grid, (rows - 1, 0))
    partial_a_reached = step_to_garden(grid, remaining_steps_from_corner)
    partial_b_reached = step_to_garden(grid, remaining_steps_from_corner + cols)
    total_reached += partial_a_reached + full_axes_grids * (partial_a_reached + partial_b_reached)

    set_starting_point(grid, (0, 0))
    partial_a_reached = step_to_garden(grid, remaining_steps_from_corner)
    partial_b_reached = step_to_garden(grid, remaining_steps_from_corner + cols)
    total_reached += partial_a_reached + full_axes_grids * (partial_a_reached + partial_b_reached)

    set_starting_point(grid, (rows - 1, cols - 1))
    partial_a_reached = step_to_garden(grid, remaining_steps_from_corner)
    partial_b_reached = step_to_garden(grid, remaining_steps_from_corner + cols)
    total_reached += partial_a_reached + full_axes_grids * (partial_a_reached + partial_b_reached)

    set_starting_point(grid, (0, cols - 1))
    partial_a_reached = step_to_garden(grid, remaining_steps_from_corner)
    partial_b_reached = step_to_garden(grid, remaining_steps_from_corner + cols)
    total_reached += partial_a_reached + full_axes_grids * (partial_a_reached + partial_b_reached)

    set_starting_point(grid, initial_starting_point)
    return total_reached

print('Part 2: ', solve_part_2(grid, 26501365)) # 637537341306357 is the right answer
