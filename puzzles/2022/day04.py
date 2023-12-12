import logging
import re

test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def part1(text_input: str) -> str:
    result = 0
    for line in text_input.strip().split("\n"):
        matches = re.match(LINE_REGEX, line)
        a, b, c, d = map(int, matches.groups())
        # Fully cover : a <= c and b >= d
        if a <= c and b >= d:
            result += 1
        elif c <= a and d >= b:
            result += 1

    return str(result)


# x1 <= y2 && y1 <= x2
def part2(text_input: str) -> str:
    result = 0
    for line in text_input.strip().split("\n"):
        matches = re.match(LINE_REGEX, line)
        a, b, c, d = map(int, matches.groups())
        # Overlap
        if a <= d and c <= b:
            result += 1
    return str(result)
