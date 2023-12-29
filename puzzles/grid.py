import numpy as np

DIR_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR_8 = DIR_4 + [(1, 1), (-1, 1), (1, -1), (-1, -1)]


def neighbors(
    pos: tuple[int, int],
    directions: list[tuple[int, int]] = DIR_4,
    filter_func: callable = lambda n: True,
):
    """Return the neighbors of pos."""
    for direction in directions:
        neighbor = tuple(np.add(pos, direction))
        if filter_func(neighbor):
            yield neighbor
