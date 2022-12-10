from typing import List, Tuple, Iterator
from collections import defaultdict


def parse_coord(coord_str: str) -> Tuple[int, int]:
    x_str, y_str = coord_str.split(",")
    return int(x_str.strip()), int(y_str.strip())


def inclusive_range(a, b):
    if b >= a:
        yield from range(a, b+1)
    else:
        yield from range(b, a+1)


class Volcano:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def __repr__(self):
        return f"Volcano[[{self.x0},{self.y0}]->[{self.x1},{self.y1}]]"

    def is_orthogonal(self):
        return self.x1 == self.x0 or self.y1 == self.y0

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        dy = self.y1 - self.y0
        dx = self.x1 - self.x0
        if not dx:
            yield from ((self.x0, y) for y in inclusive_range(self.y0, self.y1))
        elif not dy:
            yield from ((x, self.y0) for x in inclusive_range(self.x0, self.x1))
        else:
            assert abs(dx) == abs(dy)
            length = abs(dy)+1
            dx = -1 if dx < 0 else 1
            dy = -1 if dy < 0 else 1
            x = self.x0
            y = self.y0
            while length:
                yield x, y
                x += dx
                y += dy
                length -= 1


# parse volcanoes
volcanoes: List[Volcano] = []
volcanoes_ignored = []
with open("05.data") as f:
    for line in f:
        line = line.strip()
        if line:
            start_str, end_str = line.split(" -> ")
            x0, y0 = parse_coord(start_str)
            x1, y1 = parse_coord(end_str)
            volcano = Volcano(x0, y0, x1, y1)
            volcanoes.append(volcano)
print(f"got volcanoes: {len(volcanoes)}, ignored: {len(volcanoes_ignored)}")

# create field
overlaps = defaultdict(int)
for v in volcanoes:
    for coords in v:
        overlaps[coords] += 1
result = sum(1 for x in overlaps.values() if x >= 2)
print(f"overlapping positions: {result}")
