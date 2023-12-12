import logging
import re
from collections import defaultdict
from pprint import pprint

from ..utils import bfs, print_bool_grid, print_grid

test_input = """.....
.S-7.
.|.|.
.L-J.
....."""

# test_input = """-L|F7
# 7S-7|
# L|7||
# -L-J|
# L|-JF
# """
#
test_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

# test_input = """...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ...........
# """

# test_input = """.F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ...
# """

test_input = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

logger = logging.getLogger(__name__)


def parse_input(text_input: str):
    # Return (starting_position, connected)
    grid = [list(line) for line in text_input.strip().split("\n")]
    connected = {}
    starting_position = None
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            connected[y, x] = []
            if grid[y][x] == "F":
                connected[y, x] = [(y + 1, x), (y, x + 1)]
            elif grid[y][x] == "L":
                connected[y, x] = [(y - 1, x), (y, x + 1)]
            elif grid[y][x] == "J":
                connected[y, x] = [(y - 1, x), (y, x - 1)]
            elif grid[y][x] == "7":
                connected[y, x] = [(y, x - 1), (y + 1, x)]
            elif grid[y][x] == "-":
                connected[y, x] = [(y, x - 1), (y, x + 1)]
            elif grid[y][x] == "|":
                connected[y, x] = [(y - 1, x), (y + 1, x)]
            elif grid[y][x] == "S":
                starting_position = (y, x)

    # Find all that connect to the starting position
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (y, x) in connected and starting_position in connected[y, x]:
                connected[starting_position].append((y, x))

    outbounds = lambda y, x: y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0])
    actual_connection = (
        lambda y, x, y1, x1: not outbounds(y1, x1) and grid[y1][x1] != "."
    )
    connected = {
        (y, x): [
            (y1, x1) for y1, x1 in connected[y, x] if actual_connection(y, x, y1, x1)
        ]
        for y, x in connected
    }

    return starting_position, connected


def part1(text_input: str) -> str:
    starting_position, connected = parse_input(text_input)
    visited, distances = bfs(starting_position, connected)
    # Max of distances:
    return str(max(distances.values()))


def part2(text_input: str) -> str:
    grid = [list(line) for line in text_input.strip().split("\n")]
    starting_position, connected = parse_input(text_input)
    visited, distances = bfs(starting_position, connected)

    # Count tiles inside the loop, use the non-zero rule
    # https://en.wikipedia.org/wiki/Nonzero-rule
    # If a ray from a point crosses the boundary an odd number of times, it is inside the loop
    # Only consider north facing connections (eg F--J counts as 1, F--7 counts as 0)
    inside_loop = []
    for y in range(len(grid)):
        inside = False
        # When up down is odd, we are inside the loop
        for x in range(len(grid[0])):
            if grid[y][x] in ("|", "J", "L") and (y, x) in visited:
                inside = not inside
            elif grid[y][x] == "S" and (y - 1, x) in connected[(y, x)]:
                # Starting position count as a north connection
                inside = not inside
            elif inside and (y, x) not in visited:
                inside_loop.append((y, x))
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (y, x) in inside_loop:
                print("X", end="")
            else:
                print(grid[y][x], end="")
        print()

    return str(len(inside_loop))
