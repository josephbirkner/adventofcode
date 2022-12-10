from pathlib import Path
import numpy as np

reg_x = 1
cycle = 0
score = 0


def inc_cycle():
    global cycle, score, reg_x
    cycle += 1
    if ((cycle - 20) % 40) == 0:
        print(f"At cycle {cycle}: {reg_x=}")
        score += reg_x * cycle


with open(Path(__file__).parent/"10.txt") as f:
    for line in f:
        inc_cycle()
        line = line.strip()
        if line == "noop":
            continue
        # e.g. 'addx 5'
        inc_cycle()
        delta_x = int(line[5:])
        reg_x += delta_x

print(f"Done: {score=}")
