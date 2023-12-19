import logging
import re

import numpy as np

from ..utils import print_grid

test_input = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

logger = logging.getLogger(__name__)


def tilt_north(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == ".":
                # Check if there is a 0 below before any #
                for y2 in range(y + 1, len(grid)):
                    if grid[y2][x] == "O":
                        grid[y2][x] = "."
                        grid[y][x] = "O"
                        break
                    elif grid[y2][x] == "#":
                        break


def total_grid(grid):
    return sum(
        np.count_nonzero(grid[y] == "O") * (len(grid) - y) for y in range(len(grid))
    )


def part1(text_input: str) -> int | str:
    grid = np.array(list(map(list, text_input.strip().split("\n"))))
    print_grid(grid)
    tilt_north(grid)
    print("\n\n")
    print_grid(grid)
    return total_grid(grid)


memory = {}
values = []

# Convert grid to string (as a hash for memory)
grid_string = lambda g: "\n".join("".join(l) for l in g)
# Convert string to grid
string_grid = lambda s: np.array(list(map(list, s.split("\n"))))


def tilt_cycle(grid, step: int) -> tuple[int, int]:
    """
    Tilt N, W, S, E
    return cycle_end, cycle_start
    """
    gs = grid_string(grid)
    if gs in memory:
        logger.info(f"Found a loop at step {step}")
        return (step, memory[gs])
    # Rotate to simulate tilt directions
    for _ in range(4):
        tilt_north(grid)
        grid = np.rot90(grid, k=3)

    memory[gs] = step
    values.append(gs)
    return (0, 0)


def part2(text_input: str) -> int | str:
    grid = np.array(list(map(list, text_input.strip().split("\n"))))
    n = 1_000_000_000
    cycle_end, cycle_start = 0, 0
    for i in range(n):
        cycle_end, cycle_start = tilt_cycle(grid, i)
        if cycle_end != 0:
            break
    logger.info(f"Cycle detected from {cycle_start} to {cycle_end}")
    cycle_len = cycle_end - cycle_start
    target = cycle_start + ((n - cycle_start) % cycle_len)
    return total_grid(string_grid(values[target]))
