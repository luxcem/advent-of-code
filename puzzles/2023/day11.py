import logging
from pprint import pprint

from ..utils import print_grid

test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

logger = logging.getLogger(__name__)


def expand(grid, size):
    """Return a distance grid (cost of crossing each cell)."""
    distance_grid = [[1] * len(grid[0]) for _ in range(len(grid))]
    # Replace empty rows with size
    for y in range(len(grid)):
        if "#" not in grid[y]:
            distance_grid[y] = [size] * len(grid[y])
    # Replace empty columns with size
    for x in range(len(grid[0])):
        if "#" not in [grid[y][x] for y in range(len(grid))]:
            for y in range(len(grid)):
                distance_grid[y][x] = size
    return distance_grid


def get_distances(galaxies, distance_grid):
    """Return distances for each pairs of galaxies."""
    distances = {}
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            y1, x1 = galaxies[i]
            y2, x2 = galaxies[j]
            distance = 0
            # Walk the Manhattan distance between the two galaxies
            for y in range(min(y1, y2) + 1, max(y1, y2) + 1):
                distance += distance_grid[y][x1]
            for x in range(min(x1, x2) + 1, max(x1, x2) + 1):
                distance += distance_grid[y2][x]

            distances[(y1, x1), (y2, x2)] = distance
    return distances


def get_galaxies(grid):
    galaxies = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                galaxies.append((y, x))
    return galaxies


def part1(text_input: str) -> str:
    grid = text_input.strip().split("\n")
    grid = [list(line) for line in grid]
    distance_grid = expand(grid, 2)

    galaxies = get_galaxies(grid)
    # Count distance for every pair of galaxies
    distances = get_distances(galaxies, distance_grid)

    return str(sum(distances.values()))


def part2(text_input: str) -> str:
    grid = text_input.strip().split("\n")
    grid = [list(line) for line in grid]
    distance_grid = expand(grid, 1_000_000)
    galaxies = get_galaxies(grid)
    distances = get_distances(galaxies, distance_grid)

    return str(sum(distances.values()))
