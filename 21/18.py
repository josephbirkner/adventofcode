import json
from typing import Tuple, Optional, List, Union
import math
import itertools


class Number:
    value: Union[int, List['Number']]
    exploded: bool

    def __init__(self, raw_value):
        self.exploded = False
        if isinstance(raw_value, int):
            self.value = raw_value
        elif isinstance(raw_value, list):
            assert isinstance(raw_value, list)
            self.value = []
            for entry in raw_value:
                self.value.append(Number(entry))
        elif isinstance(raw_value, Number):
            self.value = raw_value.value

    def __repr__(self):
        if isinstance(self.value, list):
            return f"[{','.join(repr(c) for c in self.value)}]"
        else:
            return str(self.value)

    def __add__(self, other: 'Number'):
        old_me = Number(self)
        self.value = [old_me, other]
        self.reduce()
        return self

    def is_literal(self):
        return isinstance(self.value, int)

    def is_literal_pair(self):
        return isinstance(self.value, list) and \
               all(x.is_literal() for x in self.value) and \
               len(self.value) == 2

    def add_around(self, l, skip, r) -> Tuple[int, int]:
        assert isinstance(self.value, list)
        # identify position of skip
        pos = self.value.index(skip)
        assert pos >= 0
        if pos > 0 and l:
            l = self.value[pos-1].add_at(-1, l)
        if pos < (len(self.value) - 1) and r:
            r = self.value[pos+1].add_at(0, r)
        return l, r

    def add_at(self, where, what) -> int:
        if self.is_literal():
            self.value += what
            return 0
        elif len(self.value):
            return self.value[where].add_at(where, what)
        else:
            print("Dead end!")
            return what

    def explode(self, parents: List['Number']=None) -> bool:
        parents = parents or []
        if len(parents) > 3 and self.is_literal_pair():
            # explode self
            self.exploded = True
            skip = self
            l, r = self.value[0].value, self.value[1].value
            for parent in parents:
                l, r = parent.add_around(l, skip, r)
                if not r and not l:
                    break
                skip = parent
            return True
        elif isinstance(self.value, list):
            for child in self.value:
                exploded = child.explode([self]+parents)
                if exploded:
                    if child.exploded:
                        self.value = [
                            (c if c != child else Number(0))
                            for c in self.value
                        ]
                    return True
        return False

    def split(self) -> bool:
        if self.is_literal():
            if self.value > 9:
                half_value = self.value/2.
                self.value = [
                    Number(math.floor(half_value)),
                    Number(math.ceil(half_value))]
                return True
        else:
            for child in self.value:
                if child.split():
                    return True
        return False

    def reduce(self):
        while True:
            print(self)
            exploded = self.explode()
            if exploded:
                continue
            if not self.split():
                break

    def magnitude(self) -> int:
        if self.is_literal():
            return self.value
        else:
            assert len(self.value) == 2
            return 3*self.value[0].magnitude() + 2*self.value[1].magnitude()

    def clone(self):
        return Number(self.to_raw())

    def to_raw(self):
        if self.is_literal():
            return self.value
        else:
            return [x.to_raw() for x in self.value]


numbers = []
with open("18.data") as f:
    for line in f:
        numbers.append(Number(json.loads(line)))


result = numbers[0].clone()
for n in numbers[1:]:
    result = result.clone() + n.clone()
print(result)
print(result.magnitude())

# find largest combination
max_sum = 0
for a, b in itertools.combinations(numbers, 2):
    max_sum = max(
        max_sum,
        (a.clone() + b.clone()).magnitude(),
        (b.clone() + a.clone()).magnitude())
print("highest magnitude is", max_sum)
