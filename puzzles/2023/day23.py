import logging

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from puzzles.grid import neighbors

from ..grid import DIR_4, neighbors
from ..utils import print_grid

test_input = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

logger = logging.getLogger(__name__)


def build_graph(grid, start, end):
    G = nx.DiGraph()
    G.add_node(start)
    visited = set()
    queue = [(start, start, 0, None)]
    filter_neighbors = (
        lambda n: 0 <= n[0] < grid.shape[0]
        and 0 <= n[1] < grid.shape[1]
        and grid[n] != "#"
    )
    while queue:
        node, from_, dist, last_node = queue.pop(0)
        if (node, from_) in visited:
            continue
        visited.add((node, from_))
        if node == end:
            G.add_node(node)
            G.add_edge(from_, node, weight=dist)
            continue
        if grid[node] in "<>^v":
            # Check if last node is in the correct direction
            if last_node is None:
                continue
            if node != tuple(np.add(last_node, DIR_4[">v<^".index(grid[node])])):
                continue
            G.add_node(node)
            G.add_edge(from_, node, weight=dist)
            neighbor = tuple(np.add(node, DIR_4[">v<^".index(grid[node])]))
            if filter_neighbors(neighbor):
                queue.append((neighbor, node, 1, node))
        else:
            n_list = list(neighbors(node, filter_func=filter_neighbors))
            for neighbor in n_list:
                queue.append((neighbor, from_, dist + 1, node))

    return G


def build_graph_2(grid, start, end):
    G = nx.Graph()
    G.add_node(start)
    visited = set()
    queue = [(start, start, 0, None)]
    filter_neighbors = (
        lambda n: 0 <= n[0] < grid.shape[0]
        and 0 <= n[1] < grid.shape[1]
        and grid[n] != "#"
    )
    while queue:
        node, from_, dist, last_node = queue.pop(0)
        if (node, from_) in visited:
            continue
        visited.add((node, from_))
        if node == end:
            G.add_node(node)
            G.add_edge(from_, node, weight=dist)
            continue
        n_list = list(neighbors(node, filter_func=filter_neighbors))
        # Remove last node from neighbors avoid going back
        n_list = [n for n in n_list if n != last_node]
        if len(n_list) >= 2:
            G.add_node(node)
            G.add_edge(from_, node, weight=dist)
            for neighbor in n_list:
                queue.append((neighbor, node, 1, node))
        else:
            for neighbor in n_list:
                queue.append((neighbor, from_, dist + 1, node))

    return G


def part1(text_input: str) -> int | str:
    grid = np.array([list(line) for line in text_input.strip().split("\n")])
    print_grid(grid)
    start = (0, grid[0].tolist().index("."))
    end = (grid.shape[0] - 1, grid[-1].tolist().index("."))
    G = build_graph(grid, start, end)
    nx.draw(G, with_labels=True)
    plt.show()
    paths = nx.all_simple_paths(G, start, end)
    print(paths)


def part2(text_input: str) -> int | str:
    for _ in "<>^v":
        text_input = text_input.replace(_, ".")
    grid = np.array([list(line) for line in text_input.strip().split("\n")])
    # print_grid(grid)
    start = (0, grid[0].tolist().index("."))
    end = (grid.shape[0] - 1, grid[-1].tolist().index("."))
    G = build_graph_2(grid, start, end)
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos=pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    plt.show()
    # paths = nx.all_simple_paths(G, start, end)
    # paths = [(path, nx.path_weight(G, path, weight="weight")) for path in paths]
    # paths = sorted(paths, key=lambda x: x[1])
    return paths[-1][1]
