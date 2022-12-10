from pathlib import Path
import numpy as np


knot_pos = np.zeros((10, 2))

instr_map = {
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, -1]),
    "D": np.array([0, 1]),
}

visited_positions = set()
visited_positions.add((0, 0))

with open(Path(__file__).parent/"09.txt") as f:
    for line in f:
        line = line.strip()
        direction = instr_map[line[0]]
        steps = int(line[2:])
        while steps > 0:
            steps -= 1
            knot_pos[0] += direction
            for i in range(1, len(knot_pos)):
                dist = knot_pos[i-1] - knot_pos[i]
                abs_dist = np.abs(dist)
                sum_dist = np.sum(abs_dist)
                if sum_dist < 2:
                    continue
                if np.all(np.equal(abs_dist, 1)):
                    continue
                dist[dist < 0] = -1
                dist[dist > 0] = 1
                knot_pos[i] += dist
                assert np.all(np.less(np.abs(knot_pos[i-1] - knot_pos[i]), 2))
            visited_positions.add(tuple(knot_pos[9]))

print(len(visited_positions))

