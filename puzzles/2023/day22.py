import logging
from collections import namedtuple
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

test_input = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Point({self.x},{self.y},{self.z})"

    def __iter__(self):
        return iter((self.x, self.y, self.z))


class Brick:
    def __init__(self, p1, p2, id):
        self.p1 = p1
        self.p2 = p2
        self.id = id
        self.rest_on = []

    def __repr__(self):
        return f"Brick({self.p1}, {self.p2}, {self.id})"

    def __iter__(self):
        return iter((self.p1, self.p2, self.id))

    def fall(self, dz):
        self.p1.z += dz
        self.p2.z += dz


logger = logging.getLogger(__name__)


def draw_grid(grid):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # Create figure and 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    unique_values = np.unique(grid)[1:]

    # Create a color map for each unique value
    cmap = plt.cm.get_cmap("hsv", len(unique_values) + 1)

    for i, value in enumerate(unique_values):
        voxels = grid == value
        ax.voxels(voxels, facecolors=cmap(i), edgecolor="k")

    # Set labels and show plot
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")
    x, y, z = grid.shape
    ax.set_xlim(0, x)
    ax.set_ylim(0, y)
    ax.set_zlim(1, z)
    ax.set_box_aspect([1, 1, 1])  # This line ensures equal aspect ratio

    plt.show()


def fall(bricks, grid):
    """Simulate bricks falling."""
    for brick in bricks:
        p1, p2, id = brick
        if p1.z == 1 or p2.z == 1:
            continue
        # Find the lowest point where the brick can fall
        min_z = p1.z
        for z in range(p1.z - 1, 0, -1):
            area = grid[p1.x : p2.x + 1, p1.y : p2.y + 1, z]
            if np.any(area != 0):
                min_z = z + 1
                break
        else:
            min_z = 1
        if min_z != p1.z:
            dz = min_z - p1.z
            grid[p1.x : p2.x + 1, p1.y : p2.y + 1, p1.z : p2.z + 1] = 0
            grid[p1.x : p2.x + 1, p1.y : p2.y + 1, p1.z + dz : p2.z + dz + 1] = id
            brick.fall(dz)
            logger.info(f"Brick {brick} can fall to {min_z}")
        else:
            logger.info(f"Brick {brick} cannot fall")

        # Update rest on : bricks just under the current brick (excluding 0)
        area_under = grid[p1.x : p2.x + 1, p1.y : p2.y + 1, p1.z - 1]
        rest_on = np.unique(area_under)
        rest_on = rest_on[rest_on != 0]
        brick.rest_on = rest_on.tolist()


def prep_input(text_input: str) -> list[Brick]:
    bricks = []
    for i, line in enumerate(text_input.strip().split("\n")):
        p1, p2 = line.split("~")
        p1 = Point(*map(int, p1.split(",")))
        p2 = Point(*map(int, p2.split(",")))
        bricks.append(Brick(p1, p2, i + 1))

    # Order bricks by z coordinate
    bricks = sorted(bricks, key=lambda brick: min(brick.p1.z, brick.p2.z))
    # Create a 3D grid for bricks
    max_x = max(brick.p2.x for brick in bricks)
    max_y = max(brick.p2.y for brick in bricks)
    max_z = max(brick.p2.z for brick in bricks)
    grid = np.zeros((max_x + 1, max_y + 1, max_z + 1), dtype=int)
    for brick in bricks:
        grid[
            brick.p1.x : brick.p2.x + 1,
            brick.p1.y : brick.p2.y + 1,
            brick.p1.z : brick.p2.z + 1,
        ] = brick.id
    fall(bricks, grid)
    return bricks


def part1(text_input: str) -> int | str:
    bricks = prep_input(text_input)
    safely_removable = set(brick.id for brick in bricks)
    # Safely remove bricks
    for brick in bricks:
        if len(brick.rest_on) == 1:
            safely_removable -= set(brick.rest_on)
    return len(safely_removable)


def part2(text_input: str) -> int | str:
    bricks = prep_input(text_input)

    resting_tree = {}  # Map brick id to the bricks resting on it
    for brick in bricks:
        resting_tree[brick.id] = brick.rest_on

    counts = [0 for _ in bricks]
    for brick in bricks:
        rt = deepcopy(resting_tree)
        # Count total of brick that would fall if brick was removed
        queue = [brick.id]
        while queue:
            brick_id = queue.pop()
            for resting_brick_id in rt:
                if brick_id in rt[resting_brick_id]:
                    rt[resting_brick_id].remove(brick_id)
                    if len(rt[resting_brick_id]) == 0:
                        queue.append(resting_brick_id)
                        counts[brick.id - 1] += 1

    return sum(counts)
