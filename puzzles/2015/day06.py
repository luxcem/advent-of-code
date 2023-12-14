import logging
import re

import numpy as np

test_input = """
toggle 0,0 through 999,999
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"(.*) (\d+),(\d+) through (\d+),(\d+)")


def part1(text_input: str) -> int | str:
    matrix = np.zeros((1000, 1000), dtype=int)
    for line in text_input.strip().split("\n"):
        matches = re.match(LINE_REGEX, line)
        command, x1, y1, x2, y2 = matches.groups()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if command == "turn on":
            matrix[x1 : x2 + 1, y1 : y2 + 1] = 1
        elif command == "turn off":
            matrix[x1 : x2 + 1, y1 : y2 + 1] = 0
        elif command == "toggle":
            matrix[x1 : x2 + 1, y1 : y2 + 1] = np.logical_not(
                matrix[x1 : x2 + 1, y1 : y2 + 1]
            )
    return np.sum(matrix)


def part2(text_input: str) -> int | str:
    matrix = np.zeros((1000, 1000), dtype=int)
    for line in text_input.strip().split("\n"):
        matches = re.match(LINE_REGEX, line)
        command, x1, y1, x2, y2 = matches.groups()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if command == "turn on":
            matrix[x1 : x2 + 1, y1 : y2 + 1] += 1
        elif command == "turn off":
            matrix[x1 : x2 + 1, y1 : y2 + 1] -= 1
            matrix[matrix < 0] = 0
        elif command == "toggle":
            matrix[x1 : x2 + 1, y1 : y2 + 1] += 2
    return np.sum(matrix)
