import logging
import re
import sys

import numpy as np

from ..utils import print_bool_grid, print_grid

sys.setrecursionlimit(10000)

test_input = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

logger = logging.getLogger(__name__)

memory = {}


def propagate_beam(grid, position, direction, energized_grid):
    y, x = position
    dy, dx = direction
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return
    if memory.get((position, direction), False):
        return

    energized_grid[y][x] = True
    memory[(position, direction)] = True

    if grid[y][x] == ".":
        propagate_beam(grid, (y + dy, x + dx), direction, energized_grid)
    elif grid[y][x] == "|":
        # Split beam vertically
        propagate_beam(grid, (y + 1, x), (1, 0), energized_grid)
        propagate_beam(grid, (y - 1, x), (-1, 0), energized_grid)
    elif grid[y][x] == "-":
        # Split beam horizontally
        propagate_beam(grid, (y, x + 1), (0, 1), energized_grid)
        propagate_beam(grid, (y, x - 1), (0, -1), energized_grid)
    elif grid[y][x] == "/":
        propagate_beam(grid, (y - dx, x - dy), (-dx, -dy), energized_grid)
    elif grid[y][x] == "\\":
        propagate_beam(grid, (y + dx, x + dy), (dx, dy), energized_grid)
    else:
        return


def part1(text_input: str) -> int | str:
    grid = np.array(list(map(list, text_input.strip().split("\n"))))
    energized_grid = np.zeros_like(grid, dtype=bool)
    print_grid(grid)
    propagate_beam(grid, (0, 0), (0, 1), energized_grid)

    print("\n\n")
    print_bool_grid(energized_grid)
    # Count # in energized grid
    return np.count_nonzero(energized_grid)


def part2(text_input: str) -> int | str:
    grid = np.array(list(map(list, text_input.strip().split("\n"))))
    max_energy = 0
    # Try every border positions (top, bottom, left, right)
    starting_conditions = []
    cols = len(grid[0])
    rows = len(grid)
    for col in range(cols):
        starting_conditions.append(((0, col), (1, 0)))  # (y, x), (dy, dx)
        starting_conditions.append(((rows - 1, col), (-1, 0)))  # (y, x), (dy, dx)
    for row in range(rows):
        starting_conditions.append(((row, 0), (0, 1)))  # (y, x), (dy, dx)
        starting_conditions.append(((row, cols - 1), (0, -1)))  # (y, x), (dy, dx)

    for position, direction in starting_conditions:
        energized_grid = np.zeros_like(grid, dtype=bool)
        memory.clear()
        propagate_beam(grid, position, direction, energized_grid)
        energy = np.count_nonzero(energized_grid)
        logger.info(f"Energy at {position} is {energy}")
        if energy > max_energy:
            max_energy = energy

    return max_energy
