import logging
import re

test_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> str:
    total = 0
    lines = text_input.strip().split("\n")
    for line in lines:
        # Regex to remove all non-numeric characters
        line_clean = re.sub("[^0-9]", "", line)
        logger.info(line)
        # first and last digits:
        first = line_clean[0]
        last = line_clean[-1]
        total += int(f"{first}{last}")
    return str(total)


def part2(text_input: str) -> str:
    replace = {
        "one": "o1e",
        "two": "t2o",
        "three": "t3e",
        "four": "f4r",
        "five": "f5e",
        "six": "s6x",
        "seven": "s7n",
        "eight": "e8t",
        "nine": "n9e",
    }

    total = 0
    lines = text_input.strip().split("\n")
    for line in lines:
        # print(line)
        # First replace all words with numbers
        for word, number in replace.items():
            line = line.replace(word, number)
        # Regex to remove all non-numeric characters
        line_clean = re.sub("[^0-9]", "", line)
        # print(line_clean)
        # first and last digits:
        first = line_clean[0]
        last = line_clean[-1]
        number = int(f"{first}{last}")
        # print(number)
        total += number
    return str(total)
