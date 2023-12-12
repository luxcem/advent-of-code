import re
from collections import defaultdict

test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def part1(text_input: str) -> str:
    result = 0
    lines = text_input.strip().split("\n")
    for line in lines:
        # Match : Card (\d+):(list) | (list)
        matches = re.match(r"Card +(\d+): +(.+) \| (.+)", line)
        wining_numbers = map(int, matches.group(2).split())
        numbers = map(int, matches.group(3).split())
        # Count numbers that are in both lists
        n = len(set(wining_numbers) & set(numbers))
        result += 2 ** (n - 1) if n > 0 else 0
    return str(result)


def part2(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    my_cards = [1] * len(lines)
    for i, line in enumerate(lines):
        matches = re.match(r"Card +(\d+): +(.+) \| (.+)", line)
        wining_numbers = map(int, matches.group(2).split())
        numbers = map(int, matches.group(3).split())
        n = len(set(wining_numbers) & set(numbers))
        for j in range(i + 1, i + 1 + n):
            my_cards[j] += my_cards[i]
    return str(sum(my_cards))
