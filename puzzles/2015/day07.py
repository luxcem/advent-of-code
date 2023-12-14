import logging
import re
from functools import cache
from pprint import pprint

import numpy as np

test_input = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

logger = logging.getLogger(__name__)

values = {}


class Expression:
    def __init__(self, text: str, name=""):
        self.text = text
        self.value = None
        self.name = name
        self.ref = None
        self.operator = None
        if text.isdigit():
            self.value = int(text)
        elif text.isalpha():
            self.ref = text
        else:
            if "NOT" in text:
                self.operator = "NOT"
                self.a = Expression(text.split(" ")[1])
            elif "AND" in text:
                self.operator = "AND"
                self.a, self.b = map(Expression, text.split(" AND "))
            elif "OR" in text:
                self.operator = "OR"
                self.a, self.b = map(Expression, text.split(" OR "))
            elif "LSHIFT" in text:
                self.operator = "LSHIFT"
                self.a, self.b = map(Expression, text.split(" LSHIFT "))
            elif "RSHIFT" in text:
                self.operator = "RSHIFT"
                self.a, self.b = map(Expression, text.split(" RSHIFT "))
            else:
                raise ValueError(f"Unknown operator in {text}")

    @cache
    def evaluate(self) -> int:
        if self.value is not None:
            return self.value
        elif self.ref is not None:
            return values[self.ref].evaluate()
        else:
            if self.operator == "NOT":
                return ~self.a.evaluate()
            elif self.operator == "AND":
                return self.a.evaluate() & self.b.evaluate()
            elif self.operator == "OR":
                return self.a.evaluate() | self.b.evaluate()
            elif self.operator == "LSHIFT":
                return self.a.evaluate() << self.b.evaluate()
            elif self.operator == "RSHIFT":
                return self.a.evaluate() >> self.b.evaluate()
            else:
                raise ValueError(f"Unknown operator {self.operator}")

    def __repr__(self):
        return f"Expression({self.text})"


def part1(text_input: str) -> int | str:
    for line in text_input.strip().split("\n"):
        # Parse expression
        expression, name = line.split(" -> ")
        values[name] = Expression(expression, name)

    return values["a"].evaluate()


def part2(text_input: str) -> int | str:
    for line in text_input.strip().split("\n"):
        # Parse expression
        expression, name = line.split(" -> ")
        values[name] = Expression(expression, name)

    values["b"].value = values["a"].evaluate()
    # Reset cache
    Expression.evaluate.cache_clear()
    return values["a"].evaluate()
