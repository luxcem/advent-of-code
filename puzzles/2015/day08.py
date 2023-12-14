import logging
import re

import numpy as np

test_input = """
""
"abc"
"aaa\"aaa"
"\x27"
"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> int | str:
    result = 0
    for line in text_input.strip().split("\n"):
        result += len(line)
        line = line[1:-1]
        line = line.replace(r"\\", " ")
        line = line.replace(r"\"", " ")
        line = re.sub(r"\\x[0-9a-f]{2}", " ", line)
        result -= len(line)

    return result


def part2(text_input: str) -> int | str:
    result = 0
    for line in text_input.strip().split("\n"):
        result -= len(line)
        line = line.replace("\\", "\\\\")
        line = line.replace('"', '\\"')
        line = f'"{line}"'
        result += len(line)

    return result
