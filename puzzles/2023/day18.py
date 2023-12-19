import logging
import re

import numpy as np
import shapely

from ..utils import print_bool_grid, print_grid

test_input = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"(\w) (\d+) \(\#(\w+)\)")


def polygon_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area


def part1(text_input: str) -> int | str:
    position = (0, 0)
    corners = [position]
    last_direction = ""
    border_distance = 0
    for line in text_input.strip().split("\n"):
        direction, distance, color = LINE_REGEX.match(line).groups()
        distance = int(distance)
        border_distance += distance
        # Dug distance in direction from position
        if direction == "R":
            position = (position[0], position[1] + distance)
        elif direction == "L":
            position = (position[0], position[1] - distance)
        elif direction == "U":
            position = (position[0] - distance, position[1])
        elif direction == "D":
            position = (position[0] + distance, position[1])
        if direction != last_direction:
            corners.append(position)
        last_direction = direction
    print(shapely.Polygon(corners).buffer(0.5, join_style="mitre").area)
    return int(polygon_area(corners) + border_distance / 2 + 1)


def part2(text_input: str) -> int | str:
    position = (0, 0)
    corners = [position]
    last_direction = ""
    border_distance = 0
    for line in text_input.strip().split("\n"):
        direction, distance, color = LINE_REGEX.match(line).groups()
        # Hex to dec
        distance = int(color[:5], 16)
        direction = ["R", "D", "L", "U"][int(color[5], 16)]
        border_distance += distance
        # Dug distance in direction from position
        if direction == "R":
            position = (position[0], position[1] + distance)
        elif direction == "L":
            position = (position[0], position[1] - distance)
        elif direction == "U":
            position = (position[0] - distance, position[1])
        elif direction == "D":
            position = (position[0] + distance, position[1])
        if direction != last_direction:
            corners.append(position)
        last_direction = direction
    return int(polygon_area(corners) + border_distance / 2 + 1)
