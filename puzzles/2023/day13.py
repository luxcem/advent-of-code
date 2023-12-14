import logging
import re

import numpy as np
from puzzles.utils import print_grid

test_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"")


def line_to_bin(line: list) -> int:
    return int("".join(line).replace(".", "0").replace("#", "1"), 2)


def check_symmetry(line, correct=False):
    for i in range(1, len(line)):
        sym_len = min(i, len(line) - i)
        # Select last sym_len bits and reverse
        a = np.array(line[:i][-sym_len:][::-1])
        # Select first sym_len bits
        b = np.array(line[i:][:sym_len])
        if correct:
            # Try to correct if only one element is different and this element is a power of 2
            if np.sum(a != b) == 1 and ((diff := a ^ b) & (diff - 1) == 0).all():
                return i
        else:
            if np.all(a == b):
                return i
    return 0


def check_grid(grid, correct=False):
    # print_grid(grid)
    rows = [line_to_bin(line) for line in grid]
    cols = [line_to_bin(line) for line in zip(*grid)]
    logger.info(f"Rows: {rows}")
    row_sym = check_symmetry(rows)
    row_sym = check_symmetry(rows, correct=correct)
    logger.info(f"Cols: {cols}")
    col_sym = check_symmetry(cols)
    col_sym = check_symmetry(cols, correct=correct)
    return row_sym, col_sym


def part1(text_input: str) -> str:
    grids = text_input.strip().split("\n\n")
    total_row_sym = 0
    total_col_sym = 0
    for section in grids:
        grid = [list(line) for line in section.strip().split("\n")]
        row_sym, col_sym = check_grid(grid)
        logger.info(f"Row symmetry: {row_sym}")
        logger.info(f"Col symmetry: {col_sym}")
        total_row_sym += row_sym
        total_col_sym += col_sym

    logger.info(f"Total row symmetry: {total_row_sym}")
    logger.info(f"Total col symmetry: {total_col_sym}")
    return str(total_row_sym * 100 + total_col_sym)


def part2(text_input: str) -> str:
    grids = text_input.strip().split("\n\n")
    total_row_sym = 0
    total_col_sym = 0
    for section in grids:
        grid = [list(line) for line in section.strip().split("\n")]
        row_sym, col_sym = check_grid(grid, correct=True)
        logger.info(f"Corrected row symmetry: {row_sym}")
        logger.info(f"Corrected col symmetry: {col_sym}")
        total_row_sym += row_sym
        total_col_sym += col_sym

    logger.info(f"Total row symmetry: {total_row_sym}")
    logger.info(f"Total col symmetry: {total_col_sym}")
    return str(total_row_sym * 100 + total_col_sym)
