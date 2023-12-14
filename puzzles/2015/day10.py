import logging
import re

import numpy as np

test_input = """
3113322113
"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> int | str:
    for i in range(40):
        text_input = re.sub(
            r"(\d)\1*", lambda m: f"{len(m.group(0))}{m.group(1)}", text_input
        )
        logger.info(f"{i}: {text_input}")
    return len(text_input)


def part2(text_input: str) -> int | str:
    for i in range(50):
        text_input = re.sub(
            r"(\d)\1*", lambda m: f"{len(m.group(0))}{m.group(1)}", text_input
        )
        logger.info(f"{i}: {text_input}")
    return len(text_input)
