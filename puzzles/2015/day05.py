"""Advent of Code 2015 day 5 solution"""
import logging
import re

test_input = """"""

logger = logging.getLogger(__name__)


def is_nice(s: str):
    # It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    vowels = re.compile(r"[aeiou]")
    if len(vowels.findall(s)) < 3:
        return False
    # It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    if not re.search(r"(.)\1", s):
        return False
    # It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    if re.search(r"ab|cd|pq|xy", s):
        return False
    return True


def part1(text_input: str) -> int | str:
    count = 0
    for line in text_input.splitlines():
        logger.info(f"line: {line}")
        if is_nice(line):
            count += 1
    return count


def is_nice2(s: str):
    # It contains a pair of any two letters that appears at least twice in the string without overlapping,
    # like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    if not re.search(r"(..).*\1", s):
        return False
    # It contains at least one letter which repeats with exactly one letter between them,
    # like xyx, abcdefeghi (efe), or even aaa.
    if not re.search(r"(.).\1", s):
        return False
    return True


def part2(text_input: str) -> int | str:
    count = 0
    for line in text_input.splitlines():
        logger.info(f"line: {line}")
        if is_nice2(line):
            count += 1
    return count
