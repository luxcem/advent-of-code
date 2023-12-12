import logging
import re

test_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> str:
    carriers = text_input.strip().split("\n\n")
    l = [sum(map(int, carry.split("\n"))) for carry in carriers]
    return str(max(l))


def part2(text_input: str) -> str:
    carriers = text_input.strip().split("\n\n")
    l = sorted([sum(map(int, carry.split("\n"))) for carry in carriers])
    return str(sum(l[-3:]))
