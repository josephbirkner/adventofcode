from pathlib import Path
import dataclasses as dc
from typing import List, Dict, Tuple
from tqdm import tqdm
from copy import deepcopy
from sympy import primefactors
from collections import defaultdict
import numpy as np


monkeys: List['Monkey'] = []
all_items: List['Item'] = []


class Item:
    orig: int
    modulated: Dict[int, int]

    def __init__(self, num: int):
        global all_items
        self.modulated = {}
        self.orig = num
        all_items.append(self)

    def add_modulo(self, m: int):
        self.modulated[m] = self.orig % m

    def mul(self, n: int):
        for m, mx in self.modulated.items():
            self.modulated[m] = (mx * n) % m

    def add(self, n: int):
        for m, mx in self.modulated.items():
            self.modulated[m] = (mx + n) % m

    def test(self, m: int):
        return self.modulated[m] == 0

    def square(self):
        for m, mx in self.modulated.items():
            self.modulated[m] = (mx * mx) % m


@dc.dataclass
class Monkey:
    id: int
    items: List[Item]
    operation: str
    operand: str
    test: int
    true_dest: int
    false_dest: int
    inspections: int = 0

    def take_turn(self):
        assert self.false_dest != self.id and self.true_dest != self.id
        items = self.items.copy()
        self.items.clear()
        self.inspections += len(items)
        for item in items:
            if self.operand == "old":
                if self.operation == "*":
                    item.square()
                else:
                    item.mul(2)
            elif self.operation == "*":
                item.mul(int(self.operand))
            else:
                assert self.operation == "+"
                item.add(int(self.operand))
            # For Task 1:
            # item //= 3
            if item.test(self.test):
                monkeys[self.true_dest].items.append(item)
            else:
                monkeys[self.false_dest].items.append(item)


# Parse monkeys
with open(Path(__file__).parent/"11.txt") as f:
    lines = [line.strip() for line in f]
    for line_idx in range(0, len(lines), 7):
        mon_items, mon_op, mon_div, mon_dst_true, mon_dst_false = (
            lines[line_idx + 1:line_idx + 6])
        mon = Monkey(
            id=len(monkeys),
            items=list(map(
                lambda s: Item(int(s)),
                mon_items[16:].split(", "))),
            operation=mon_op[21],
            operand=mon_op[23:],
            test=int(mon_div[19:]),
            true_dest=int(mon_dst_true[25:]),
            false_dest=int(mon_dst_false[26:]))
        monkeys.append(mon)

# Register required modulos for all monkeys
for mon in monkeys:
    for item in all_items:
        item.add_modulo(mon.test)


# Run sim
def sim(steps: int):
    for round_num in tqdm(range(steps)):
        for mon in monkeys:
            mon.take_turn()
    for mon in monkeys:
        print(mon.inspections)


sim(10000)

mon1, mon2 = sorted([mon.inspections for mon in monkeys], reverse=True)[:2]
print(mon1 * mon2)
