from typing import List, Tuple, Set, Iterator

grid = []
with open("09.data") as f:
    for line in f:
        grid.append(list(map(int, line.strip())))
threats = 0


def neighbors(lx, ly, criterion) -> Iterator[Tuple[int, int]]:
    if lx > 0 and criterion(grid[ly][lx - 1]):
        yield lx-1, ly
    if lx < len(line) - 1 and criterion(grid[ly][lx + 1]):
        yield lx+1, ly
    if ly > 0 and criterion(grid[ly - 1][lx]):
        yield lx, ly-1
    if ly < len(grid) - 1 and criterion(grid[ly + 1][lx]):
        yield lx, ly+1


# Initialize basins
risk = 0
basins: List[Set[Tuple[int, int]]] = []
for y, line in enumerate(grid):
    for x, n in enumerate(line):
        if not any(neighbors(x, y, lambda nn: nn <= n)):
            risk += n+1
            basins.append({(x, y)})
print(f"Starting out with {len(basins)} basins ({risk=}).")


# Grow basins
it_n = 0
while True:
    changed = False
    print(f"========== Iteration {it_n} ==========")
    for i, basin_field in enumerate(basins):
        new_basin_field = basin_field.copy()
        for x, y in basin_field:
            for nx, ny in neighbors(x, y, lambda nn: True):
                if grid[y][x] < grid[ny][nx] < 9:
                    new_basin_field.add((nx, ny))
        if len(new_basin_field) > len(basin_field):
            print(f"Basin {i} grew to {len(new_basin_field)}.")
            basin_field |= new_basin_field
            changed = True
    if not changed:
        break
    it_n += 1


# Select largest basins
basins.sort(key=lambda b: len(b), reverse=True)
print(list(len(b) for b in basins))

print(len(basins[0])*len(basins[1])*len(basins[2]))
