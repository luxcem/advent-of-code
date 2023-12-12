import re

test_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def part1(text_input: str) -> str:
    maxes = {"red": 12, "green": 13, "blue": 14}
    lines = text_input.strip().split("\n")
    total = 0
    for line in lines:
        valid_game = True
        # Match regex : Game (id) : (line)
        matches = re.match(r"Game (\d+): (.*)", line)
        game_id = int(matches.group(1))
        game_line = matches.group(2)
        draws = map(str.strip, game_line.split(";"))
        for draw in draws:
            colors = list(map(str.split, draw.split(",")))
            for color in colors:
                color_number = int(color[0])
                color_name = color[1]
                if color_number > maxes[color_name]:
                    valid_game = False
                    break

        if valid_game:
            # add game id to total
            total += game_id
    return str(total)


def part2(text_input: str) -> str:
    lines = text_input.strip().split("\n")
    total = 0
    for line in lines:
        minimums = {"red": 0, "green": 0, "blue": 0}
        # Match regex : Game (id) : (line)
        matches = re.match(r"Game (\d+): (.*)", line)
        game_id = int(matches.group(1))
        game_line = matches.group(2)
        draws = map(str.strip, game_line.split(";"))
        for draw in draws:
            colors = list(map(str.split, draw.split(",")))
            for color in colors:
                color_number = int(color[0])
                color_name = color[1]
                if color_number > minimums[color_name]:
                    minimums[color_name] = color_number
        # Multiply mimimums
        total += minimums["red"] * minimums["green"] * minimums["blue"]
    return str(total)
