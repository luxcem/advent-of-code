import logging
import re

test_input = """A Y
B X
C Z"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"")

scores_1 = {
    "A": {"X": 3 + 1, "Y": 6 + 2, "Z": 0 + 3},
    "B": {"X": 0 + 1, "Y": 3 + 2, "Z": 6 + 3},
    "C": {"X": 6 + 1, "Y": 0 + 2, "Z": 3 + 3},
}

scores_2 = {
    "A": {"X": 0 + 3, "Y": 3 + 1, "Z": 6 + 2},
    "B": {"X": 0 + 1, "Y": 3 + 2, "Z": 6 + 3},
    "C": {"X": 0 + 2, "Y": 3 + 3, "Z": 6 + 1},
}


def part1(text_input: str) -> str:
    result = 0
    for line in text_input.strip().split("\n"):
        other, mine = line.split(" ")
        result += scores_1[other][mine]
    return str(result)


def part2(text_input: str) -> str:
    result = 0
    for line in text_input.strip().split("\n"):
        other, mine = line.split(" ")
        result += scores_2[other][mine]
    return str(result)
