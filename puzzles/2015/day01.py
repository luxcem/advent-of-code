import logging
import re

test_input = """))((((("""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> str:
    # Count ( and )
    result = 0
    for line in text_input.strip().split("\n"):
        result += line.count("(") - line.count(")")
    return str(result)


def part2(text_input: str) -> str:
    floor = 0
    for i, c in enumerate(text_input.strip(), 1):
        floor += 1 if c == "(" else -1
        if floor < 0:
            return str(i)
    return "0"
