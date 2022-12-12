from pathlib import Path

import numpy
import numpy as np


UNKOWN_DIST = 999999
OFFSETS = [[1, 0], [0, 1], [-1, 0], [0, -1]]


def parse_heightmap():
    result = []
    s = None
    e = None
    with open(Path(__file__).parent/"12.txt") as f:
        for y, row in enumerate(f):
            result.append([])
            row = row.strip()
            for x, col in enumerate(row):
                if col == "S":
                    s = np.array([x, y])
                    result[-1].append(0)
                elif col == "E":
                    e = np.array([x, y])
                    result[-1].append(25)
                else:
                    result[-1].append(ord(col) - ord('a'))
    result = np.array(result).transpose()
    return result, s, e


def surrounding(where: np.ndarray, field: np.ndarray):
    for offset in OFFSETS:
        pos = where + offset
        if np.any(np.less(pos, 0)) or np.any(np.greater_equal(pos, field.shape)):
            continue
        yield pos, field[pos[0], pos[1]]


heightmap, start, end = parse_heightmap()
distance_map = np.zeros(heightmap.shape)
distance_map[:, :] = UNKOWN_DIST
distance_map[end[0], end[1]] = 0


def update():
    global distance_map, heightmap
    old_dist_map = distance_map.copy()
    for own_pos, own_dist in numpy.ndenumerate(distance_map):
        if own_dist == UNKOWN_DIST:
            continue
        own_height = heightmap[own_pos[0], own_pos[1]]
        for pos, height in surrounding(np.array(own_pos), heightmap):
            if height >= own_height - 1:
                dist = distance_map[pos[0], pos[1]]
                if dist > own_dist + 1:
                    distance_map[pos[0], pos[1]] = own_dist + 1
    return not np.all(np.equal(distance_map, old_dist_map))


count = 0
while True:
    count += 1
    print(f"Update {count}: {100-np.sum(np.equal(distance_map, UNKOWN_DIST).astype(int))/np.prod(distance_map.shape)*100:.2f}%")
    if not update():
        break

# Distance from start to end
print(distance_map[start[0], start[1]])

# Distance from any square at elevation 0 to end
distances_from_0 = []
for pos, height in numpy.ndenumerate(heightmap):
    if height == 0:
        distances_from_0.append(distance_map[pos[0], pos[1]])

distances_from_0.sort()
print(distances_from_0)
