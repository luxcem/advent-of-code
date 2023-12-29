import logging
import re
from collections import defaultdict

import numpy as np

from ..grid import neighbors
from ..utils import print_bool_grid, print_grid, render_grid

test_input = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

logger = logging.getLogger(__name__)

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def march(
    grid: np.ndarray,
    starts: list[tuple[int, int]],
) -> set[tuple[int, int]]:
    new_starts = set()
    for start in starts:
        for n in neighbors(start, grid.shape):
            if grid[n] != "#":
                new_starts.add(n)
    return new_starts


def part1(text_input: str) -> int:
    grid = np.array([list(line) for line in text_input.strip().split("\n")])
    starts = set((len(grid) // 2, len(grid[0]) // 2))
    for i in range(64):
        new_starts = set()
        starts = march(grid, starts)
    return len(starts)


def possible_points(point, garden_map):
    # Loop over all possible directions, and yield each possible new point
    # Check the remainder of the point axis' divided by 131 to continue moving outward infinitely for part 2
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for d in directions:
        new_point = (point[0] + d[0], point[1] + d[1])
        if (
            garden_map[new_point[1] % 131][new_point[0] % 131] != "#"
        ):  # Make sure it wasn't a rock
            yield new_point


def bfs(point, garden_map, max_dist):
    # Use the Breadth first search to find the number of points hit each step, and return the dictionary with key of number of steps taken,
    # and value of number of points hit
    tiles = defaultdict(int)
    visited = set()
    queue = [(point, 0)]
    while queue:  # End when the queue is empty
        curr_point, dist = queue.pop(0)
        if (
            dist == (max_dist + 1) or curr_point in visited
        ):  # Don't include points that have already been visited
            continue

        tiles[dist] += 1
        visited.add(curr_point)

        for next_point in possible_points(
            curr_point, garden_map
        ):  # Loop over possible points and add to queue
            queue.append((next_point, (dist + 1)))
    return tiles


def calculate_possible_spots(start, garden_map, max_steps):
    # Get the output from bfs, and then return the sum of all potential stopping points in the tiles output based on even numbers
    tiles = bfs(start, garden_map, max_steps)
    return sum(
        amount for distance, amount in tiles.items() if distance % 2 == max_steps % 2
    )


def quad(y, n):
    # Use the quadratic formula to find the output at the large steps based on the first three data points
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return (a * n**2) + (b * n) + c


def parse_input(data):
    # Find the start point, and then split the input into a nested list and return the start point and the garden map
    data_list = data.splitlines()
    for idx, line in enumerate(data_list):
        start = re.search(r"S", line)
        if start is not None:
            start = (start.start(), idx)
            break
    data_list = [list(line) for line in data_list]
    return (start, data_list)


def part2(text_input: str) -> int:
    parsed_data = parse_input(text_input)
    # Calculate the first three data points for use in the quadratic formula, and then return the output of quad
    goal = 26501365
    size = len(parsed_data[1])
    edge = size // 2

    y = [calculate_possible_spots(*parsed_data, (edge + i * size)) for i in range(3)]

    return quad(y, ((goal - edge) // size))


"""
def part2(text_input: str) -> int | str:
    grid = np.array([list(line) for line in text_input.strip().split("\n")])
    grid = np.tile(grid, (5, 5))
    # Replace "S" with "."
    grid[grid == "S"] = "."
    # render_grid(grid == ".")
    starts = set((len(grid) // 2, len(grid[0]) // 2))

    for i in range(130):
        new_starts = set()
        starts = march(grid, starts)
    return len(starts)

    # render_grid(grid == ".")
    # print_grid(grid)
"""
