from typing import Any

import numpy as np


def print_grid(grid):
    """Print a 2d grid."""
    # Use the largest cell as cell width
    cell_width = max([len(str(x)) for row in grid for x in row])
    for row in grid:
        print(" ".join([str(x).rjust(cell_width) for x in row]))


def print_bool_grid(grid):
    """Print a 2d grid."""
    for row in grid:
        print(" ".join(["#" if x else "." for x in row]))


def bfs(start, connections, end=None):
    """
    Perform a breadth-first search on a grid.

    Parameters
    ----------
    start : tuple
        The starting position (y, x) on the grid.
    connections : dict
        A dict of connections for each position on the grid.
        eg: {(y, x): [(y, x), ...]}
    end : tuple, optional
        The end position (y, x) on the grid.
        if not provided, the search will continue until all positions are visited.

    Returns
    -------
    visited : set
        The set of positions visited during the search.
    distances : dict
        The distance from the starting position to each position visited.
    """

    visited = set()
    distances = {}
    queue = [(start, 0)]
    while queue:
        position, distance = queue.pop(0)
        if position in visited:
            continue
        visited.add(position)
        distances[position] = distance
        if position == end:
            return visited, distances
        for neighbor in connections[position]:
            queue.append((neighbor, distance + 1))

    return visited, distances


class BinNode:
    def __init__(self, name: str):
        self.name: str = name
        self.left: BinNode | None = None
        self.right: BinNode | None = None

    def __str__(self):
        return self.name


def print_bin_tree(node: BinNode | None, level: int = 0, direction: str = "root"):
    if node is None:
        return
    dire = "(L)" if direction == "left" else "(R)" if direction == "right" else ""
    print(f"{'  ' * level}{dire} {node}")
    print_bin_tree(node.left, level + 1, "left")
    print_bin_tree(node.right, level + 1, "right")


def render_grid(grid, size=5):
    import pygame

    # Calculate grid dimensions
    rows, cols = grid.shape
    screen_width = cols * size
    screen_height = rows * size

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))  # Fill the screen with white

        # Render the grid based on boolean values
        for row in range(rows):
            for col in range(cols):
                color = (
                    (0, 0, 0) if grid[row][col] else (255, 255, 255)
                )  # Black for True, White for False
                pygame.draw.rect(screen, color, (col * size, row * size, size, size))

        pygame.display.flip()
        clock.tick(60)
