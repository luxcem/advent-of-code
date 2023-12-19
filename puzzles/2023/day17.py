import logging
from heapq import heappop, heappush

import numpy as np

from ..utils import print_bool_grid, print_grid

test_input = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


logger = logging.getLogger(__name__)

directions = ((1, 0), (-1, 0), (0, 1), (0, -1))


def add_to_queue(
    queue, grid, heat_loss: int, y: int, x: int, dy: int, dx: int, steps: int = 1
):
    new_y = y + dy
    new_x = x + dx
    if new_y < 0 or new_y >= len(grid) or new_x < 0 or new_x >= len(grid[0]):
        return
    heappush(queue, (heat_loss + grid[new_y][new_x], new_y, new_x, dy, dx, steps))


def part1(text_input: str) -> int:
    grid = np.array(list(map(list, text_input.strip().split("\n"))))
    grid = grid.astype(int)
    visited = set()

    queue = [(0, 0, 0, 0, 0, 0)]
    while queue:
        heat_loss, y, x, dy, dx, steps = heappop(queue)
        if (y, x) == (len(grid) - 1, len(grid[0]) - 1):
            return heat_loss
        if (y, x, dy, dx, steps) in visited:
            continue
        visited.add((y, x, dy, dx, steps))
        if steps < 3 and (dy, dx) != (0, 0):
            # Continue in the same direction
            add_to_queue(queue, grid, heat_loss, y, x, dy, dx, steps + 1)
        # Turn
        for new_dy, new_dx in directions:
            if (new_dy, new_dx) != (dy, dx) and (new_dy, new_dx) != (-dy, -dx):
                add_to_queue(queue, grid, heat_loss, y, x, new_dy, new_dx)

    return -1


def print_path(grid, path):
    path_grid = np.zeros_like(grid)
    for pos in path:
        path_grid[pos[0], pos[1]] = 1
    print_bool_grid(path_grid)


def part2(text_input: str) -> int | str:
    grid = np.array(list(map(list, text_input.strip().split("\n"))))
    grid = grid.astype(int)
    visited = set()

    queue = [(0, 0, 0, 0, 0, 0)]
    while queue:
        heat_loss, y, x, dy, dx, steps = heappop(queue)
        if (y, x, dy, dx, steps) in visited:
            continue
        visited.add((y, x, dy, dx, steps))

        if (y, x) == (len(grid) - 1, len(grid[0]) - 1):
            print_path(grid, visited)
            return heat_loss

        # Minimum of 4 steps in the same direction
        if steps < 4 and (dy, dx) != (0, 0):
            # Continue in the same direction
            add_to_queue(queue, grid, heat_loss, y, x, dy, dx, steps + 1)
        else:
            if steps < 10 and (dy, dx) != (0, 0):
                add_to_queue(queue, grid, heat_loss, y, x, dy, dx, steps + 1)
            # Turn
            for new_dy, new_dx in directions:
                if (new_dy, new_dx) != (dy, dx) and (new_dy, new_dx) != (-dy, -dx):
                    add_to_queue(queue, grid, heat_loss, y, x, new_dy, new_dx)

    return -1
