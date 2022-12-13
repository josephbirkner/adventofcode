from pathlib import Path
import json
import numpy as np
from typing import Union, List, Optional
import dataclasses as dc

packets = []


class Value:
    val: Union[int, List['Value']]

    def __init__(self, datum: Union[List, int]):
        if isinstance(datum, int):
            self.val = datum
        else:
            assert isinstance(datum, list)
            self.val = list(map(Value, datum))

    def compare(self, other: 'Value', indent=0) -> Optional[bool]:
        if isinstance(self.val, int) and isinstance(other.val, int):
            print("  "*indent + f"- Compare {self.val} vs {other.val}")
            if self.val > other.val:
                print("  " * (indent + 1) + f"- Right side is smaller")
                return False
            elif self.val < other.val:
                return True
            else:
                return None
        elif isinstance(self.val, int):
            return Value([self.val]).compare(other, indent)
        elif isinstance(other.val, int):
            return self.compare(Value([other.val]), indent)
        else:
            print("  " * indent + f"- Compare {self.val} vs {other.val}")
            i = 0
            j = 0
            same_length = len(self.val) == len(other.val)
            while True:
                if i >= len(self.val):
                    if same_length:
                        return None
                    return True
                if j >= len(other.val):
                    print("  " * (indent+1) + f"- Right side ran out of items")
                    return False
                result = self.val[i].compare(other.val[j], indent+1)
                if result is not None:
                    return result
                i += 1
                j += 1

    def __lt__(self, other):
        return self.compare(other) is True

    def __repr__(self):
        return repr(self.val)


with open(Path(__file__).parent/"13.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        packets.append(Value(json.loads(line)))

right_order = []
for packet_index in range(0, len(packets), 2):
    p1, p2 = packets[packet_index:packet_index+2]
    if p1.compare(p2):
        right_order.append(packet_index//2+1)

print("=========== Task 1 ===========")

print(right_order)
print(sum(right_order))

print("=========== Task 2 ===========")

# Task 2
start = Value([[2]])
stop = Value([[6]])
packets += [start, stop]
packets.sort()
for p in packets:
    print(p)
start_i = packets.index(start)+1
stop_i = packets.index(stop)+1
print(start_i, stop_i)
print(start_i * stop_i)
