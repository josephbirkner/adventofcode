from pathlib import Path
from typing import Set, Tuple, List, Dict, Optional, Union, Iterator
import numpy as np
from tqdm import tqdm


occupied: Set[Tuple[int, int]] = set()
sensor_min_beacon_dist: Union[np.ndarray, List[Tuple[int, int, int]]] = []


# Parse beacon/sensor locations
with open(Path(__file__).parent/"15.txt") as f:
    for line in f:
        # "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
        line_parts = line.strip()[12:].split(": closest beacon is at x=")
        coords = [np.array(list(map(int, coords.split(", y=")))) for coords in line_parts]
        dist = np.sum(np.abs(coords[1] - coords[0]))
        occupied.add(tuple(coords[0]))
        occupied.add(tuple(coords[1]))
        sensor_min_beacon_dist.append((int(coords[0][0]), int(coords[0][1]), int(dist)))

# Determine field extents
sensor_min_beacon_dist = np.array(sensor_min_beacon_dist)
max_range = np.max(sensor_min_beacon_dist[:, 2])
min_x = np.min(sensor_min_beacon_dist[:, 0])
max_x = np.max(sensor_min_beacon_dist[:, 0])
min_y = np.min(sensor_min_beacon_dist[:, 1])
max_y = np.max(sensor_min_beacon_dist[:, 1])
print(f"{max_range=} {min_x=} {max_x=} {min_y=} {max_y=}")


# Function to gather verified free cells along a row
def count_empty(y, x_min, x_max, invert=True) -> Iterator[Tuple[int, int]]:
    sample_pos = np.arange(x_max-x_min, dtype='int32') + x_min
    sample_pos = np.stack((sample_pos, np.zeros(x_max-x_min, dtype='int32')), axis=1)
    sample_pos[:, 1] = y
    dists = np.broadcast_to(sample_pos.reshape((1, -1, 2)), (len(sensor_min_beacon_dist), len(sample_pos), 2))
    dists = np.sum(np.abs(dists - sensor_min_beacon_dist[:, :2].reshape((-1, 1, 2))), axis=2)
    dists_out_of_range = np.greater(dists, sensor_min_beacon_dist[:, 2].reshape((-1, 1)))
    dists_out_of_range = dists_out_of_range.transpose()
    free_pos = np.all(dists_out_of_range, axis=1)
    if invert:
        free_pos = np.logical_not(free_pos)
    return np.sum(free_pos)


# Task 1: Sample row with y=2000000
# print(f"Verified empty: {count_empty(2000000, min_x - max_range, max_x + max_range, invert=True)-1} positions.")


def sample_edge_positions(min_x=0, min_y=0, max_x=4000000, max_y=4000000):
    print("Gathering edge positions...")
    for x, y, d in sensor_min_beacon_dist:
        edge_positions = []
        xx = x - d - 1
        yy = y
        edge_positions.append((xx, yy))
        for _ in range(d+1):
            xx += 1
            yy -= 1
            edge_positions.append((xx, yy))
        for _ in range(d+1):
            xx += 1
            yy += 1
            edge_positions.append((xx, yy))
        for _ in range(d+1):
            xx -= 1
            yy += 1
            edge_positions.append((xx, yy))
        for _ in range(d+1):
            xx -= 1
            yy -= 1
            edge_positions.append((xx, yy))
        print(f"Sampling {len(edge_positions)} edge positions...")
        edge_positions = np.array(edge_positions)
        dists = np.broadcast_to(edge_positions.reshape((1, -1, 2)), (len(sensor_min_beacon_dist), len(edge_positions), 2))
        dists = np.sum(np.abs(dists - sensor_min_beacon_dist[:, :2].reshape((-1, 1, 2))), axis=2)
        dists_out_of_range = np.greater(dists, sensor_min_beacon_dist[:, 2].reshape((-1, 1)))
        dists_out_of_range = dists_out_of_range.transpose()
        free_pos = np.all(dists_out_of_range, axis=1)
        result = edge_positions[free_pos]
        result = result[result[:, 0] >= min_x]
        result = result[result[:, 0] <= max_x]
        result = result[result[:, 1] >= min_y]
        result = result[result[:, 1] <= max_y]
        yield from result


# Task 2:
for pos in sample_edge_positions():
    print(int(pos[0])*4000000 + int(pos[1]))
    break
