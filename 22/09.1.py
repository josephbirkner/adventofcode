from pathlib import Path
import numpy as np


head_pos = np.array([0, 0])
tail_pos = np.array([0, 0])

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
            head_pos += direction
            dist = head_pos - tail_pos
            abs_dist = np.abs(dist)
            sum_dist = np.sum(abs_dist)
            if sum_dist < 2:
                continue
            if np.all(np.equal(abs_dist, 1)):
                continue
            dist[dist < 0] = -1
            dist[dist > 0] = 1
            tail_pos += dist
            visited_positions.add(tuple(tail_pos))
            assert np.all(np.less(np.abs(head_pos - tail_pos), 2))

print(len(visited_positions))

