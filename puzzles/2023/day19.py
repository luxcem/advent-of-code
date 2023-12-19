import copy
import logging
import re

import numpy as np

from ..utils import BinNode, print_bin_tree

test_input = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

logger = logging.getLogger(__name__)


class Node:
    size: int = 0

    def __init__(self, name: str, rules: str = ""):
        self.name: str = name
        self.rules: str = rules
        self.left: Node | None = None
        self.right: Node | None = None


def create_tree(node: Node, nodes: dict[str, Node]):
    """Construct a binary tree from rules."""
    # node = nodes[node_name]
    if not node.rules:
        return
    rules = node.rules.split(",")
    if len(rules) == 2:
        node.left = nodes[rules[0].split(":")[1]]
        node.right = nodes[rules[1]]
    elif len(rules) > 2:
        # Create a left node for first rule and append the rest to the right node
        node.left = nodes[rules[0].split(":")[1]]
        node.right = Node(node.name + "2", ",".join(rules[1:]))
    node.rules = rules[0].split(":")[0]
    create_tree(node.left, nodes)
    create_tree(node.right, nodes)


def eval_rule(data: dict[str, int], rule: str) -> bool:
    if rule in "AR":
        return rule == "A"
    var, op, value = re.match(r"(\w+)([<>=])(\d+)", rule).groups()
    return data[var] < int(value) if op == "<" else data[var] > int(value)


def part1(text_input: str) -> int:
    # Parse input into a binary tree starting at "in"
    workflows, rankings = text_input.strip().split("\n\n")
    workflows = workflows.split("\n")
    nodes: dict[str, Node] = {}
    for workflow in workflows:
        name, rules = re.match(r"(\w+){(.+)}", workflow).groups()
        nodes[name] = Node(name, rules)
    nodes["A"] = Node("A", "")
    nodes["R"] = Node("R", "")
    create_tree(nodes["in"], nodes)

    # Count accepted rankings
    accepted = []
    for rank in rankings.split("\n"):
        x, m, a, s = map(int, re.findall(r"(?:\w+)=(\d+)", rank))
        data = {"x": x, "m": m, "a": a, "s": s}
        node = nodes["in"]
        while node.name not in "AR":
            # if data passes node rules, go left, else go right
            node = node.left if eval_rule(data, node.rules) else node.right
        if node.name == "A":
            accepted.append(data)
    return sum(sum(data.values()) for data in accepted)


def size_of_node(node: Node, possible_values: dict[str, list[int]]) -> None:
    """Compute size of each node in the tree."""
    if node.name in "AR":
        node.size += int(
            np.prod(
                [
                    max(0, possible_values[var][1] - possible_values[var][0] + 1)
                    for var in possible_values
                ]
            )
        )
    else:
        # Run size_of_node on left and right nodes
        var, op, value = re.match(r"(\w+)([<>])(\d+)", node.rules).groups()
        value = int(value)
        left_values = copy.deepcopy(possible_values)
        right_values = copy.deepcopy(possible_values)
        if op == "<":
            left_values[var][1] = min(left_values[var][1], value - 1)
            right_values[var][0] = max(right_values[var][0], value)
        else:
            left_values[var][0] = max(left_values[var][0], value + 1)
            right_values[var][1] = min(right_values[var][1], value)
        size_of_node(node.left, left_values)
        size_of_node(node.right, right_values)


def part2(text_input: str) -> int:
    # Parse input into a binary tree starting at "in"
    workflows = text_input.strip().split("\n\n")[0].split("\n")
    nodes: dict[str, Node] = {}
    for workflow in workflows:
        matches = re.match(r"(\w+){(.+)}", workflow)
        if not matches:
            logger.error(f"Cannot parse {workflow}")
            raise ValueError
        name = matches.group(1)
        rules = matches.group(2)
        nodes[name] = Node(name, rules)
    nodes["A"] = Node("A", "")
    nodes["R"] = Node("R", "")

    create_tree(nodes["in"], nodes)
    # print_bin_tree(nodes["in"])
    size_of_node(
        nodes["in"], {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}
    )
    return nodes["A"].size
