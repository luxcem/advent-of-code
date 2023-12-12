import re

from ..utils import print_bool_grid, print_grid

test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def part1(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    symbols = {
        (y, x): []
        for y in range(len(lines))
        for x in range(len(lines[0]))
        if lines[y][x] not in "01234566789."
    }
    for i, line in enumerate(lines):
        matches = re.finditer(r"(\d+)", line)
        for match in matches:
            edges = [
                (y, x)
                for x in range(match.start() - 1, match.end() + 1)
                for y in [i - 1, i, i + 1]
            ]
            for edge in edges:
                if edge in symbols:
                    symbols[edge].append(int(match.group(1)))
    return str(sum(map(sum, symbols.values())))


def part2(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    symbols = {
        (y, x): []
        for y in range(len(lines))
        for x in range(len(lines[0]))
        if lines[y][x] == "*"
    }
    for i, line in enumerate(lines):
        matches = re.finditer(r"(\d+)", line)
        for match in matches:
            edges = [
                (y, x)
                for x in range(match.start() - 1, match.end() + 1)
                for y in [i - 1, i, i + 1]
            ]
            for edge in edges:
                if edge in symbols:
                    symbols[edge].append(int(match.group(1)))
    total = 0
    for symbol in symbols:
        if len(symbols[symbol]) == 2:
            total += symbols[symbol][0] * symbols[symbol][1]
    return str(total)


directions = [
    (0, -1),  # Up
    (1, 0),  # Right
    (0, 1),  # Down
    (-1, 0),  # Left
    (1, -1),  # Up-Right
    (1, 1),  # Down-Right
    (-1, 1),  # Down-Left
    (-1, -1),  # Up-Left
]


def mark_number(grid, valid_grid, coordinates):
    """Mark a coordinate as valid."""
    # Check for valid coordinates
    x, y = coordinates
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        return
    # If coordinate is already valid or is a dot return
    if valid_grid[y][x] or grid[y][x] == ".":
        return
    valid_grid[y][x] = True
    # If grid[x][y] is a number return it
    if grid[y][x].isnumeric():
        # Find the number on this coordinate (left or right)
        number = ""
        # Check left
        x_left = x
        while x_left >= 0 and grid[y][x_left].isnumeric():
            number = grid[y][x_left] + number
            valid_grid[y][x_left] = True
            x_left -= 1
        # Check right
        x_right = x + 1
        while x_right < len(grid[0]) and grid[y][x_right].isnumeric():
            number += grid[y][x_right]
            valid_grid[y][x_right] = True
            x_right += 1
        # print(f"Found number {number} at {x},{y}")
        return int(number)
    # If grid[x][y] is not a dot mark all adjacent coordinates as valid (all directions)
    elif grid[y][x] != ".":
        return list(
            filter(
                bool,
                [
                    mark_number(grid, valid_grid, (x + direction[0], y + direction[1]))
                    for direction in directions
                ],
            )
        )


def part1_old(text_input: str) -> str:
    # Transform input into a 2x2 grid
    grid = list(map(list, text_input.strip().split("\n")))
    valid_grid = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    print_grid(grid)
    # Loop through grid and mark any valid coordinates
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # If char is not a number and not a dot "."
            if not grid[y][x].isnumeric() and grid[y][x] != ".":
                print(f"Found {grid[y][x]} at {x},{y}")
                # Mark as valid
                numbers = mark_number(grid, valid_grid, (x, y))
                total += sum(map(int, numbers))

    return str(total)


def part2_old(text_input: str) -> str:
    # Transform input into a 2x2 grid
    grid = list(map(list, text_input.strip().split("\n")))
    valid_grid = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    # Loop through grid and mark any valid coordinates
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # If char is not a number and not a dot "."
            if grid[y][x] == "*":
                # Mark as valid
                numbers = mark_number(grid, valid_grid, (x, y))
                if len(numbers) == 2:
                    total += numbers[0] * numbers[1]
    return str(total)
