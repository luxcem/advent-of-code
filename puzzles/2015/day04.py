"""Advent of Code 2015 day 4 solution"""
# Md5
import hashlib
import logging
import re

test_input = """ckczppom"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> str:
    secret_key = text_input.strip()
    i = 0
    while True:
        i += 1
        hash = hashlib.md5(f"{secret_key}{i}".encode("utf-8")).hexdigest()
        if hash.startswith("00000"):
            return str(i)


def part2(text_input: str) -> str:
    secret_key = text_input.strip()
    i = 0
    while True:
        i += 1
        hash = hashlib.md5(f"{secret_key}{i}".encode("utf-8")).hexdigest()
        if hash.startswith("000000"):
            return str(i)
