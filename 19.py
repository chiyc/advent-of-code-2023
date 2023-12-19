import re
from typing import Mapping, NewType, TypedDict

from input import read_input


Name = NewType('Name', str)


class Condition:
    def __init__(self, category: str, comparison: str, rating: int):
        self.category = category
        self.comparison = comparison
        self.rating = rating

    def passes(self, part):
        if self.comparison == '<':
            return part[self.category] < self.rating
        elif self.comparison == '>':
            return part[self.category] > self.rating
        else:
            assert False

class Rule:
    def __init__(self, destination: Name, condition: Condition=None):
        self.destination = destination
        self.condition = condition

    def evaluate(self, part):
        if self.condition is None or self.condition.passes(part):
            return self.destination
        else:
            return None


class Part(TypedDict):
    x: int
    m: int
    a: int
    s: int


class Workflow:
    def __init__(self, name: Name, rules: list[Rule]):
        self.name = name
        self.rules = rules

    def send(self, part):
        for rule in self.rules:
            destination = rule.evaluate(part)
            if destination:
                return Name(destination)
        assert False


class System:
    def __init__(self, workflows: Mapping[Name, Workflow], parts: list[Part]):
        self.workflows = workflows
        self.parts = parts
        self.accepted_parts = []
        self.rejected_parts = []

    def initialize(input_generator):
        workflows: Mapping[Name, Workflow] = {}
        line = next(input_generator)
        while line != '':
            matched = re.match(r'(\w+)\{([\d<>:\w,]+)\}', line)
            name = matched.group(1)
            rules: list[Rule] = []
            _rules = matched.group(2).split(',')
            for _rule in _rules:
                if ':' in _rule:
                    _condition, destination = _rule.split(':')
                    matched = re.match(r'(\w+)([<>])(\d+)', _condition)
                    category = str(matched.group(1))
                    comparison = str(matched.group(2))
                    rating = int(matched.group(3))
                    rule = Rule(Name(destination), Condition(category, comparison, rating))
                else:
                    destination = _rule
                    category = None
                    comparison = None
                    rating = None
                    rule = Rule(Name(destination))
                rules.append(rule)
            workflows[Name(name)] = Workflow(Name(name), rules)
            line = next(input_generator)

        parts: list[Part] = []
        line = next(input_generator)
        while line:
            matched = re.match(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', line)
            x = int(matched.group(1))
            m = int(matched.group(2))
            a = int(matched.group(3))
            s = int(matched.group(4))
            part: Part = {
                'x': x,
                'm': m,
                'a': a,
                's': s,
            }
            parts.append(part)
            try:
                line = next(input_generator)
            except StopIteration:
                break

        return System(workflows, parts)

    def rate_parts(self):
        for part in self.parts:
            destination = Name('in')
            while destination not in ('A', 'R'):
                workflow = self.workflows[destination]
                destination = workflow.send(part)

            if destination == 'A':
                self.accepted_parts.append(part)
            elif destination == 'R':
                self.rejected_parts.append(part)

    def grade_accepted_parts(self):
        score = 0
        for part in self.accepted_parts:
            score += part['x'] + part['m'] + part['a'] + part['s']
        return score


system = System.initialize(read_input(19))
system.rate_parts()
print('Part 1: ', system.grade_accepted_parts()) # 389114
