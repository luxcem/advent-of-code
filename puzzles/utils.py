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
