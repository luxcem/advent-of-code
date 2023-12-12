"""Advent of Code 2015 day 2 solution"""
import logging
import re

test_input = """^v^v^v^v^v"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> str:
    current_position = (0, 0)
    positions = {current_position}

    for c in text_input.strip():
        if c == "^":
            current_position = (current_position[0], current_position[1] + 1)
        elif c == "v":
            current_position = (current_position[0], current_position[1] - 1)
        elif c == ">":
            current_position = (current_position[0] + 1, current_position[1])
        elif c == "<":
            current_position = (current_position[0] - 1, current_position[1])
        positions.add(current_position)

    return str(len(positions))


def part2(text_input: str) -> str:
    current_positions = [(0, 0), (0, 0)]
    positions = {current_positions[0]}

    for i, c in enumerate(text_input.strip()):
        current_position = current_positions[i % 2]
        if c == "^":
            current_position = (current_position[0], current_position[1] + 1)
        elif c == "v":
            current_position = (current_position[0], current_position[1] - 1)
        elif c == ">":
            current_position = (current_position[0] + 1, current_position[1])
        elif c == "<":
            current_position = (current_position[0] - 1, current_position[1])
        current_positions[i % 2] = current_position
        positions.add(current_position)

    return str(len(positions))
