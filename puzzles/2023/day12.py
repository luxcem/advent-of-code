import logging
import re
from functools import cache

test_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

logger = logging.getLogger(__name__)
memory = {}


def process_line(line: str, counts: tuple[int, ...], n=0) -> int:
    """Process a line."""
    if not counts:
        return "#" not in line
    if not line:
        return not counts

    if (line, counts) in memory:
        return memory[(line, counts)]

    result = 0
    if line[0] in ".?":
        # Replacing ? with dot : process the remaining line
        result += process_line(line[1:], counts, n + 1)
    if line[0] in "#?":
        # Meaning we can find count[0] consecutive # in the line
        if (
            counts[0] <= len(line)
            and "." not in line[: counts[0]]
            and (len(line) == counts[0] or line[counts[0]] != "#")
        ):
            result += process_line(line[counts[0] + 1 :], counts[1:], n + 1)
    memory[(line, counts)] = result
    return result


def part1(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    lines = [line.split(" ") for line in lines]
    lines = [(line[0], [int(x) for x in line[1].split(",")]) for line in lines]
    result = 0
    for line in lines:
        count = process_line(line[0], tuple(line[1]))
        result += count
    return str(result)


def part2(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    lines = [line.split(" ") for line in lines]
    lines = [(line[0], [int(x) for x in line[1].split(",")]) for line in lines]
    result = 0
    for line in lines:
        pattern = "?".join([line[0]] * 5)
        counts = tuple(line[1] * 5)
        count = process_line(pattern, counts)
        result += count
    return str(result)
