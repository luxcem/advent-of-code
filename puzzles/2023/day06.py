import logging
import re
from math import ceil, floor, prod, sqrt

test_input = """Time:      7  15   30
Distance:  9  40  200
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"")


def part1(text_input: str) -> str:
    result = 1
    times = [int(x) for x in text_input.strip().split("\n")[0].split(":")[1].split()]
    distances = [
        int(x) for x in text_input.strip().split("\n")[1].split(":")[1].split()
    ]
    for i in range(len(times)):
        # solve : x * (time - x) > distance
        time = times[i]
        distance = distances[i]
        min_time = floor(1 / 2 * (time - sqrt(time**2 - 4 * distance)))
        max_time = ceil(1 / 2 * (time + sqrt(time**2 - 4 * distance)) - 1)
        result *= max_time - min_time

    return str(result)


def part2(text_input: str) -> str:
    text_input = text_input.replace(" ", "")
    return part1(text_input)
