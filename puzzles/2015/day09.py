import logging
import re
from collections import defaultdict

import numpy as np

test_input = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"(.*) to (.*) = (\d+)")


def naive(start: str, distances: dict, remaining_cities: set, path):
    if not remaining_cities:
        return 0, path
    else:
        min_distance = np.inf
        min_path = None
        for city in remaining_cities:
            current_dist, current_path = naive(
                city, distances, remaining_cities - {city}, path + [city]
            )
            current_dist += distances[path[-1]][city]
            if current_dist < min_distance:
                min_distance = current_dist
                min_path = current_path
        return min_distance, min_path


def part1(text_input: str) -> int | str:
    distances = defaultdict(dict)
    for line in text_input.strip().split("\n"):
        matches = re.match(LINE_REGEX, line)
        distances[matches.group(1)][matches.group(2)] = int(matches.group(3))
        distances[matches.group(2)][matches.group(1)] = int(matches.group(3))

    for start in distances.keys():
        distance, path = naive(
            start, distances, set(distances.keys()) - {start}, [start]
        )
        logger.info(f"Path: {path}")
        logger.info(f"Distance: {distance}")
    return distance


def part2(text_input: str) -> int | str:
    distances = defaultdict(dict)
    for line in text_input.strip().split("\n"):
        matches = re.match(LINE_REGEX, line)
        distances[matches.group(1)][matches.group(2)] = -int(matches.group(3))
        distances[matches.group(2)][matches.group(1)] = -int(matches.group(3))

    for start in distances.keys():
        distance, path = naive(
            start, distances, set(distances.keys()) - {start}, [start]
        )
        logger.info(f"Path: {path}")
        logger.info(f"Distance: {distance}")
    return -distance
