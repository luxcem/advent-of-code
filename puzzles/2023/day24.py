import logging
from collections import namedtuple
from pprint import pprint

import numpy as np
from sympy import solve, symbols

test_input = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

logger = logging.getLogger(__name__)

Point = namedtuple("Point", "x y z")
Particle = namedtuple("Particle", "pos vel")


def find_intersection(p1: Particle, p2: Particle) -> Point | None:
    """Return the point of intersection of two particles, or None."""
    p1_pos = p1.pos
    p1_vel = p1.vel
    p2_pos = p2.pos
    p2_vel = p2.vel

    # Calculate the direction vectors for the lines
    dir1 = (p1_vel.x, p1_vel.y, p1_vel.z)
    dir2 = (p2_vel.x, p2_vel.y, p2_vel.z)

    # Calculate the cross product of the direction vectors
    cross_product = (
        dir1[1] * dir2[2] - dir1[2] * dir2[1],
        dir1[2] * dir2[0] - dir1[0] * dir2[2],
        dir1[0] * dir2[1] - dir1[1] * dir2[0],
    )

    # Calculate the dot product of the cross product with the difference of positions
    diff_pos = (p1_pos.x - p2_pos.x, p1_pos.y - p2_pos.y, p1_pos.z - p2_pos.z)
    dot_product = (
        cross_product[0] * diff_pos[0]
        + cross_product[1] * diff_pos[1]
        + cross_product[2] * diff_pos[2]
    )

    # Check if the lines are parallel (dot product of cross product and difference is close to zero)
    if abs(dot_product) < 1e-9:
        return None  # Lines are parallel, no intersection

    # Calculate the parameters for the lines to find the intersection point
    t = (
        (p2_pos.x - p1_pos.x) * dir2[1] - (p2_pos.y - p1_pos.y) * dir2[0]
    ) / dot_product

    if t < 0:
        return None
    # Calculate the intersection point
    intersection = Point(
        x=p1_pos.x + t * dir1[0],
        y=p1_pos.y + t * dir1[1],
        z=p1_pos.z + t * dir1[2],
    )
    return intersection


def find_intersection_2d(p1: Particle, p2: Particle) -> Point | None:
    """Return the point of intersection of two particles, or None."""
    x1, y1, _ = p1.pos
    x2, y2, _ = p2.pos
    vx1, vy1, _ = p1.vel
    vx2, vy2, _ = p2.vel

    # Check if the lines are parallel
    det = vx2 * vy1 - vx1 * vy2
    if det == 0:
        return None  # Lines are parallel, no intersection

    t1 = ((x1 - x2) * vy2 - (y1 - y2) * vx2) / det
    t2 = ((x1 - x2) * vy1 - (y1 - y2) * vx1) / det
    if t1 < 1 or t2 < 1:
        return None
    intersection_x = x1 + vx1 * t1
    intersection_y = y1 + vy1 * t1

    return Point(intersection_x, intersection_y, 0)


def part1(text_input: str) -> int | str:
    particles = []
    for line in text_input.strip().split("\n"):
        pos, vel = line.split(" @ ")
        pos = pos.split(", ")
        vel = vel.split(", ")
        pos = Point(*map(int, pos))
        vel = Point(*map(int, vel))
        particles.append(Particle(pos, vel))

    border = (200000000000000, 400000000000000)
    count = 0
    for i, p1 in enumerate(particles):
        for p2 in particles[i + 1 :]:
            inter = find_intersection_2d(p1, p2)
            if inter is not None:
                logger.info(f"P1: {p1}")
                logger.info(f"P2: {p2}")
                logger.info(f"Intersection found: {inter}\n")
                if border[0] < inter.x < border[1] and border[0] < inter.y < border[1]:
                    count += 1
    return count


def part2(text_input: str) -> int | str:
    particles = []
    for line in text_input.strip().split("\n"):
        pos, vel = line.split(" @ ")
        pos = pos.split(", ")
        vel = vel.split(", ")
        pos = Point(*map(int, pos))
        vel = Point(*map(int, vel))
        particles.append(Particle(pos, vel))

    # Need to find x, y, z and vx, vy, vz such that
    # x + vx * t1 = x1 + vx1 * t1
    # y + vy * t1 = y1 + vy1 * t1
    # z + vz * t1 = z1 + vz1 * t1
    # for all particles (only 6 unknowns, so 6 equations are enough)
    # We have 2 equations for each particles (eliminating t1)
    x = symbols("x")
    y = symbols("y")
    z = symbols("z")
    vx = symbols("vx")
    vy = symbols("vy")
    vz = symbols("vz")

    p1, v1 = particles[0]
    p2, v2 = particles[1]
    p3, v3 = particles[2]
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    vx1, vy1, vz1 = v1
    vx2, vy2, vz2 = v2
    vx3, vy3, vz3 = v3

    equations = [
        (x1 - x) * (vy - vy1) - (y1 - y) * (vx - vx1),
        (x1 - x) * (vz - vz1) - (z1 - z) * (vx - vx1),
        (x2 - x) * (vy - vy2) - (y2 - y) * (vx - vx2),
        (x2 - x) * (vz - vz2) - (z2 - z) * (vx - vx2),
        (x3 - x) * (vy - vy3) - (y3 - y) * (vx - vx3),
        (x3 - x) * (vz - vz3) - (z3 - z) * (vx - vx3),
    ]
    solutions = solve(equations, [x, y, z, vx, vy, vz], dict=True)
    for sol in solutions:
        if all(v == int(v) for v in sol.values()):
            return sol[x] + sol[y] + sol[z]
