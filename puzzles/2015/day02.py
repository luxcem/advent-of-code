"""Advent of Code 2015 day 2 solution"""
import logging
import re

test_input = """"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    result = 0
    for line in lines:
        x, y, z = [int(x) for x in line.split("x")]
        result += 2 * x * y + 2 * y * z + 2 * z * x + min(x * y, y * z, z * x)
    return str(result)


def part2(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    result = 0
    for line in lines:
        x, y, z = [int(x) for x in line.split("x")]
        result += x * y * z + 2 * min(x + y, y + z, z + x)
    return str(result)
