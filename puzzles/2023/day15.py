import logging
import re

import numpy as np

test_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"")

"""
    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
"""


def hash_word(word: str) -> int:
    current_value = 0
    for char in word:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def part1(text_input: str) -> int | str:
    hashes = []
    for word in text_input.strip().split(","):
        hashes.append(hash_word(word))
    logger.info(hashes)
    return sum(hashes)


def part2(text_input: str) -> int | str:
    boxes = [dict() for _ in range(256)]
    hashes = []
    for word in text_input.strip().split(","):
        if "=" in word:
            label, value = word.split("=")
            boxes[hash_word(label)][label] = value
        if "-" in word:
            # Remove value from labeled box
            label, _ = word.split("-")
            boxes[hash_word(label)].pop(label, None)

    power = 0
    for i, box in enumerate(boxes, 1):
        spot = 1
        for key, value in box.items():
            logger.info(f"Box {i} has {key} with value {value}")
            power += i * int(value) * spot
            spot += 1
    logger.info(f"Power is {power}")
    return sum(hashes)
