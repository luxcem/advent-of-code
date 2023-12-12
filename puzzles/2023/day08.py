import logging
import re
from math import lcm

# test_input = """RL

# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)
# """

# test_input = """LLR

# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)
# """

test_input = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"(\w+) = \((\w{3}), (\w{3})\)")

tree = {}
# node : (left, right)


# def dfs(tree):
#     visited = []

#     def dfs_rec(node, path):
#         if node not in visited:
#             visited.append(node)
#             if node == "ZZZ":
#                 return path
#             else:
#                 left, right = tree[node]
#                 return dfs_rec(left, path + ["L"]) or dfs_rec(right, path + ["R"])

#     return dfs_rec("AAA", [])


def do_instruction(instruction, tree, start="AAA", end="ZZZ"):
    instruction = list(instruction) * 100
    current_node = start
    steps = 0
    while instruction:
        if current_node == "ZZZ":
            return steps
        next_instruction = instruction.pop(0)
        if next_instruction == "L":
            current_node = tree[current_node][0]
        else:
            current_node = tree[current_node][1]
        steps += 1


def do_instruction2(instruction, tree, start):
    instruction = list(instruction) * 100
    current_node = start
    steps = 0
    while instruction:
        if current_node[-1] == "Z":
            return steps
        next_instruction = instruction.pop(0)
        if next_instruction == "L":
            current_node = tree[current_node][0]
        else:
            current_node = tree[current_node][1]
        steps += 1


def part1(text_input: str) -> str:
    # Parse tree
    lines = text_input.strip().split("\n")
    instruction = lines[0]
    for line in lines[2:]:
        matches = re.match(LINE_REGEX, line)
        tree[matches.group(1)] = (matches.group(2), matches.group(3))
    return str(do_instruction(instruction, tree))
    # path = dfs(tree)
    # return str(len(path))
    # return str(result)


def part2(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    instruction = lines[0]
    for line in lines[2:]:
        matches = re.match(LINE_REGEX, line)
        tree[matches.group(1)] = (matches.group(2), matches.group(3))

    starts = []
    steps = []
    for key in tree:
        if key[-1] == "A":
            starts.append(key)
    for start in starts:
        steps.append(do_instruction2(instruction, tree, start))
    return str(lcm(*steps))
