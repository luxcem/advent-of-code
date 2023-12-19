import argparse
import importlib
import logging
import os

import notebook_loader
from lib.get_input import get_input
from lib.get_input import logout as logout_session

LOG_FORMAT = "%(message)s"


def main(year: int, day: int, puzzle: int, test=False, unit_test=False) -> str:
    print(f"Advent of Code {year}")
    print(f"Day {day}, Puzzle {puzzle}")
    module = importlib.import_module(f"puzzles.{year}.day{day:02d}")
    if test:
        data_input = module.test_input
    else:
        data_input = get_input(year, day, puzzle)
    if unit_test:
        return getattr(module, f"test")()
    solution = getattr(module, f"part{puzzle}")
    return solution(data_input)


def logout() -> None:
    logout_session()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("year", type=int)
    args.add_argument("day", type=int)
    args.add_argument("puzzle", type=int, default=1, nargs="?")
    args.add_argument("--test", "-t", action="store_true")
    args.add_argument("--unit", "-u", action="store_true")
    args.add_argument("--debug", "-d", action="store_true")
    args.add_argument("--submit", "-s", action="store_true")
    args.add_argument("--logout", action="store_true")
    args = args.parse_args()

    if args.logout:
        logout()
        exit(0)

    if args.debug:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
        os.environ["DEBUG"] = "1"
    else:
        logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT)

    result = main(args.year, args.day, args.puzzle, args.test, args.unit)
    print(result)
