import logging
import re

test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"")


def part1(text_input: str) -> str:
    result = 0
    commons = []
    for line in text_input.strip().split("\n"):
        # Split line in middle
        first, second = line[: len(line) // 2], line[len(line) // 2 :]
        # Common
        for char in set(set(first) & set(second)):
            commons.append(char)
    # Map letter to value (a = 1, b = 2, ...), A = 27, B = 28, ...
    for char in commons:
        if char.isupper():
            result += ord(char) - 38
        else:
            result += ord(char) - 96

    return str(result)


def part2(text_input: str) -> str:
    result = 0
    lines = text_input.strip().split("\n")
    # Loop 3 lines each time
    for i in range(0, len(lines), 3):
        a, b, c = lines[i], lines[i + 1], lines[i + 2]
        # Common in 3 lines
        commons = set(set(a) & set(b) & set(c))
        # Map letter to value (a = 1, b = 2, ...), A = 27, B = 28, ...
        for char in commons:
            if char.isupper():
                result += ord(char) - 38
            else:
                result += ord(char) - 96

    return str(result)
