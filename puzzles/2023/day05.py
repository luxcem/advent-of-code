import logging
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


def map_interval(source, mapping, offset):
    """Map interval.

    Given a starting interval [a, b], a starting interval [s1, s2], offset o,
    return the resulting intervals after mapping.

    if b < s1 or a > s2 then return [a, b]
    if a < s1 and b > s2 then return [a, s1 - 1], [s1 + o, b + o]
    if a > s1 and b < s2 then return [s1 + o, s2 + o]
    if a > s1 and b > s2 then return [a + o, s2 + o], [s2 + 1, b]
    """
    a, b = source
    s1, s2 = mapping
    o = offset
    if b < s1 or a > s2:
        return [[a, b]]
    elif a < s1 and b > s2:
        return [[a, s1 - 1], [s1 + o, b + o]]
    elif a > s1 and b < s2:
        return [[s1 + o, s2 + o]]
    elif a > s1 and b > s2:
        return [[a + o, s2 + o], [s2 + 1, b]]


"""
OLD
def part1(text_input: str) -> str:
    result = 0
    lines = text_input.strip().split("\n")
    seeds = [int(x) for x in lines[0].split(":")[1].strip().split(" ")]
    ranges = {}
    max_seed = max(seeds)
    i = 1
    while i < len(lines):
        line = lines[i]
        if line == "":
            i += 1
            continue

        if line[-1] == ":":
            key = line.split()[0].strip()
            ranges[key] = []
            i += 1
            while i < len(lines) and lines[i] != "":
                destination_start, source_start, range_length = (
                    lines[i].strip().split(" ")
                )
                # Append to ranges: (source_start, source_end, offset)
                ranges[key].append(
                    (
                        int(source_start),
                        int(source_start) + int(range_length),
                        int(destination_start) - int(source_start),
                    )
                )
                i += 1
        i += 1

    logger.info(f"ranges: {ranges}")
    minimum_location = 99_999_999_999
    for seed in seeds:
        n_input = seed
        for key in ranges:
            logger.info(f"input: {n_input}, key: {key}")
            for source_start, source_end, offset in ranges[key]:
                if source_start <= n_input < source_end:
                    n_input += offset
                    break
            if key == "humidity-to-location":
                minimum_location = min(minimum_location, n_input)
                break

    return str(minimum_location)


def part2(text_input: str) -> str:
    result = 0
    lines = text_input.strip().split("\n\n")
    seeds = lines.pop(0)
    seeds = [int(seed) for seed in seeds.split(":")[1].split()]
    # Group seeds 2 by 2
    seeds = [(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)]
    maps_name = [line.split(":")[0].strip() for line in lines]
    maps = [line.split(":")[1].strip().split("\n") for line in lines]
    # Seeds is a list of interval eg: [(79, 93), (55, 68)]
    # For each steps we will match seeds to the corresponding destination interval.
    minimum_location = min([seed[0] for seed in seeds])
    for i, ranges in enumerate(maps):
        print(f"\nStep {i}: {maps_name[i]}")
        # print(f"Seeds: {seeds}")
        # list of transformations for this step
        ranges = [list(map(int, line.split())) for line in ranges]
        new_seeds = []
        for seed in seeds:
            intersections = []
            for range_ in ranges:
                # For each transformation we will match the list of seeds to the
                # corresponding destination interval.
                dest, source, length = range_
                source_interval = (source, source + length)
                offset = dest - source
                # print(f"{source_interval} -> {dest, dest + length}")
                # print(dest, source, length)
                # Exemple (98, 100) -> (50, 52)
                if seed[0] <= source_interval[1] and seed[1] >= source_interval[0]:
                    # Seed is in the source interval
                    # Intersecting interval with source
                    intersecting_interval = (
                        max(seed[0], source_interval[0]),
                        min(seed[1], source_interval[1]),
                    )
                    if intersecting_interval[0] > seed[0]:
                        # Seed is not at the beginning of the source interval
                        intersections.append((seed[0], intersecting_interval[0]))
                    if intersecting_interval[1] < seed[1]:
                        # Seed is not at the end of the source interval
                        intersections.append((intersecting_interval[1], seed[1]))
                    intersections.append(
                        (
                            intersecting_interval[0] + offset,
                            intersecting_interval[1] + offset,
                        )
                    )
                    if intersecting_interval[0] + offset == 0:
                        print(dest, source, length)
                        print(f"Seed {seed} is at the beginning of the interval")
                    # print(
                    #     f"Mapping {seed} to {source_interval} -> {source_interval[0] + offset, source_interval[1] + offset}"
                    # )
                    # print(f"Intersections: {intersections}")

            if intersections:
                new_seeds.extend(intersections)
            else:
                new_seeds.append(seed)
        # print(f"New seeds: {new_seeds}")
        seeds = new_seeds
    new_min = min([seed[0] for seed in seeds])
    return str(min(new_min, minimum_location))
"""
