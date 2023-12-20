import re
from collections import deque, namedtuple
from typing import Mapping, NewType, TypedDict

from input import read_input


Name = NewType('Name', str)


class Part(TypedDict):
    x: int
    m: int
    a: int
    s: int


class Range():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'[{self.start}, {self.end}]'


class RangedPart(TypedDict):
    x: Range
    m: Range
    a: Range
    s: Range


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

    def passing_range(self, ranged_part):
        range = ranged_part[self.category]
        if self.comparison == '<':
            if range.start <= self.rating:
                return RangedPart(ranged_part | {
                    self.category: Range(range.start, min(range.end, self.rating - 1))
                })
        elif self.comparison == '>':
            if range.end >= self.rating:
                return RangedPart(ranged_part | {
                    self.category: Range(max(range.start, self.rating + 1), range.end)
                })
        else:
            assert False
        return None


    def failing_range(self, ranged_part):
        range = ranged_part[self.category]
        if self.comparison == '<':
            if range.end >= self.rating:
                return RangedPart(ranged_part | {
                    self.category: Range(max(range.start, self.rating), range.end)
                })
        elif self.comparison == '>':
            if range.start <= self.rating:
                return RangedPart(ranged_part | {
                    self.category: Range(range.start, min(range.end, self.rating))
                })
        else:
            assert False
        return None


class Rule:
    def __init__(self, destination: Name, condition: Condition=None):
        self.destination = destination
        self.condition = condition

    def evaluate(self, part):
        if self.condition is None or self.condition.passes(part):
            return self.destination
        else:
            return None

    def evaluate_range(self, ranged_part):
        passing_range, failing_range = None, None
        if self.condition is None:
            passing_range = ranged_part
        else:
            passing_range = self.condition.passing_range(ranged_part)
            failing_range = self.condition.failing_range(ranged_part)
        return passing_range, failing_range


Queued = namedtuple('Queued', ['workflow', 'rule', 'part'])


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
        self.accepted_ranged_parts = []
        self.rejected_ranged_parts = []

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

    def analyze_acceptance_criteria(self):
        ranged_part_queue = deque([
            Queued(Name('in'), 0, RangedPart({
                'x': Range(1, 4000),
                'm': Range(1, 4000),
                'a': Range(1, 4000),
                's': Range(1, 4000),
            }))
        ])
        while ranged_part_queue:
            workflow_name, rule_index, part = ranged_part_queue.popleft()

            if workflow_name == 'A':
                self.accepted_ranged_parts.append(part)
            elif workflow_name == 'R':
                self.rejected_ranged_parts.append(part)
            else:
                workflow = self.workflows[workflow_name]
                rule = workflow.rules[rule_index]
                passing, failing = rule.evaluate_range(part)
                if passing:
                    ranged_part_queue.append(
                        Queued(rule.destination, 0, passing)
                    )
                if failing:
                    ranged_part_queue.append(
                        Queued(workflow_name, rule_index + 1, failing)
                    )
        possible_parts = 0
        for part in self.accepted_ranged_parts:
            x = part['x'].end - part['x'].start + 1
            m = part['m'].end - part['m'].start + 1
            a = part['a'].end - part['a'].start + 1
            s = part['s'].end - part['s'].start + 1
            possible_parts += x * m * a * s
        return possible_parts


system = System.initialize(read_input(19))
system.rate_parts()
print('Part 1: ', system.grade_accepted_parts()) # 389114
print('Part 2: ', system.analyze_acceptance_criteria()) # 125051049836302
