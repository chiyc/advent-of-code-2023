from abc import ABC, abstractmethod
from collections import deque, namedtuple
from math import lcm
from typing import Mapping

from input import read_input


# Pulse type is 0 for low, 1 for high
Pulse = namedtuple('Pulse', ['source', 'destination', 'type'])

class Module(ABC):
    name: str
    destinations: list[str]

    def receive(self, pulse):
        # self.print_pulse(pulse)
        return self._receive(pulse)

    @abstractmethod
    def _receive(self, pulse):
        pass

    @abstractmethod
    def reset(self):
        pass

    def print_pulse(self, pulse):
        pulse_type = '-low' if pulse.type == 0 else '-high'
        print(f'{pulse.source} {pulse_type}-> {pulse.destination}')

    def send(self, pulse_type):
        return [
            Pulse(self.name, dest, pulse_type)
            for dest in self.destinations
        ]


class TestModule(Module):
    name: str
    destinations: list[str] = []

    def __init__(self, name):
        self.name = name

    def _receive(self, pulse):
        return []

    def reset(self):
        pass


class BroadcastModule(Module):
    name: str = 'broadcaster'
    destinations: list[str]

    def __init__(self, destinations):
        self.destinations = destinations

    def _receive(self, pulse):
        return self.send(pulse.type)

    def reset(self):
        pass


class FlipFlopModule(Module):
    name: str
    state: any
    destinations: list[str]

    def __init__(self, name, destinations):
        self.name = name
        self.state = 0 # 0 for off, 1 for on
        self.destinations = destinations

    def _receive(self, pulse):
        prev = self.state
        self.state = int(not (self.state ^ pulse.type))
        # Ignores high pulses, flips from low pulses
        # Sends a high pulse when turning on, low if turning off
        if self.state != prev:
            return self.send(self.state)
        return []

    def reset(self):
        self.state = 0


class ConjunctionModule(Module):
    name: str
    state: any
    destinations: list[str]

    def __init__(self, name, destinations):
        self.name = name
        self.state = {} # Map each input to last pulse
        self.destinations = destinations

    def _receive(self, pulse):
        self.state[pulse.source] = pulse.type
        pulse_type = int(not all(self.state.values()))
        # Sends low pulse if receiving high for all inputs
        # Otherwise, high pulse
        return self.send(pulse_type)

    def initialize_input(self, name):
        self.state[name] = 0

    def reset(self):
        for input in self.state.keys():
            self.state[input] = 0


class Modules():
    modules: Mapping[str, Module]
    sent_pulses: Mapping[int, int] = {0: 0, 1: 0}

    def __init__(self, modules):
        self.modules = modules
        self.pulses = deque([])

    def build_modules(input_generator):
        modules: Mapping[str, Module] = {}
        conjunction_modules = set()
        for _line in input_generator:
            name_and_type, _destinations = _line.split(' -> ')
            destinations = _destinations.split(', ')

            if name_and_type == 'broadcaster':
                name = name_and_type
                module = BroadcastModule(destinations)
            else:
                name = name_and_type[1:]

                type = name_and_type[0]
                if type == '%':
                    module = FlipFlopModule(name, destinations)
                elif type == '&':

                    module = ConjunctionModule(name, destinations)
                    conjunction_modules.add(name)
            modules[name] = module

        for name, module in modules.items():
            for destination in module.destinations:
                if destination in conjunction_modules:
                    modules[destination].initialize_input(name)

        return Modules(modules)

    def press_button(self, pulse_to_record=None):
        pulse_to_record_count = 0
        self.pulses.append(Pulse('button', 'broadcaster', 0))
        while self.pulses:
            pulse = self.pulses.popleft()
            if pulse.destination not in self.modules:
                self.modules[pulse.destination] = TestModule(pulse.destination)
            self.sent_pulses[pulse.type] += 1
            if pulse == pulse_to_record:
                pulse_to_record_count += 1

            next_pulses = self.modules[pulse.destination].receive(pulse)
            self.pulses.extend(next_pulses)
        return pulse_to_record_count

    def reset(self):
        self.sent_pulses = {0: 0, 1: 0}
        for module in self.modules.values():
            module.reset()


modules = Modules.build_modules(read_input(20))
for _ in range(1000):
    modules.press_button()
print('Part 1: ', modules.sent_pulses[0] * modules.sent_pulses[1]) # 814934624


# Observed in input that rx has &nr as its single input. In order for nr
# to send a low pulse, it must receive a high pulse from all of its own inputs

# I did a manual test to confirm that these modules send a high pulse at a
# regular frequency, so we can find the least common multiple for the solution
multiples = []
for i, module in enumerate(['lh', 'fk', 'ff', 'mm']):
    modules.reset()
    n = 0
    while True:
        n += 1
        pulses = modules.press_button(pulse_to_record=Pulse(module, 'nr', 1))
        if pulses:
            multiples.append(n)
            break
print('Part 2: ', lcm(*multiples)) # 228282646835717
