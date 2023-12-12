"""Advent of Code 2023 Day 9."""
import numpy as np

test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def complete_sequence(seq):
    if all(seq == 0):
        return np.append(seq, 0)
    return np.append(seq, seq[-1] + complete_sequence(np.diff(seq))[-1])


def part1(text_input: str) -> str:
    print("They're the same picture"[::-1])
    result = 0
    for line in text_input.strip().split("\n"):
        numbers = np.array([int(x) for x in line.split()])
        seq = complete_sequence(numbers)
        result += seq[-1]
    return str(result)


def part2(text_input: str) -> str:
    result = 0
    for line in text_input.strip().split("\n"):
        numbers = np.array([int(x) for x in line.split()])
        seq = complete_sequence(numbers[::-1])
        result += seq[-1]
    return str(result)
