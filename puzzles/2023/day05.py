import logging
import os
import re
from pprint import pprint

test_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

logger = logging.getLogger(__name__)


def map_interval(interval, destination, source, length) -> tuple[list, list]:
    """Map interval.

    Given a starting interval [a, b], a source, destination and length. return
    [inside, outside] where inside is a list of intervals that are inside the
    source interval
    """
    a, b = interval
    overlap_start = max(a, source)
    overlap_end = min(b, source + length)
    if overlap_start < overlap_end:
        # Overlap
        inside = [
            (destination + overlap_start - source, destination + overlap_end - source)
        ]
        outside = []
        if a < overlap_start:
            outside.append((a, overlap_start))
        if overlap_end < b:
            outside.append((overlap_end, b))
        return inside, outside
    else:
        return [], []


def part1(text_input: str) -> int:
    lines = text_input.strip().split("\n\n")
    seeds = [int(x) for x in lines.pop(0).split(":")[1].strip().split(" ")]
    # ranges = {}
    # max_seed = max(seeds)
    logger.info(f"Seeds: {seeds}")
    for group in lines:
        group_name = group.split("\n")[0]
        logger.info(f"{group_name}")
        new_seeds = []
        for seed in seeds:
            new_seed = seed
            for mappings in group.split("\n")[1:]:
                destination, source, length = map(int, mappings.split())
                if seed >= source and seed < source + length:
                    new_seed += destination - source
                    break
            new_seeds.append(new_seed)
        seeds = new_seeds
        logger.info(f"Seeds: {new_seeds}")
    return min(seeds)


def part2(text_input: str) -> int:
    lines = text_input.strip().split("\n\n")
    seeds = [int(x) for x in lines.pop(0).split(":")[1].strip().split(" ")]
    # Convert [a, b, c, d, ...] into [(a, a+b), (c, c+d), ...]
    seeds = [(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)]
    logger.info(f"Seeds: {seeds}")
    for group in lines:
        group_name = group.split("\n")[0]
        logger.info(f"{group_name}")

        new_seeds = []
        while seeds:
            seed = seeds.pop()
            # Split interval to avoid overlapping
            for mappings in group.split("\n")[1:]:
                destination, source, length = map(int, mappings.split())
                # Check overlap
                inside, outside = map_interval(seed, destination, source, length)
                new_seeds.extend(inside)
                seeds.extend(outside)
                if inside:
                    break
            else:
                new_seeds.append(seed)
        seeds = new_seeds
    return min(seeds)[0]
