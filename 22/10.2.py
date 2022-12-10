from pathlib import Path
import numpy as np

reg_x = 1
cycle = 0
score = 0

crt_row = ""
crt_row_cnt = 0


def do_cycle():
    global cycle, score, reg_x, crt_row, crt_row_cnt
    cycle += 1
    x_pos = (cycle % 40) - 1
    if abs(x_pos - reg_x) <= 1:
        crt_row += "#"
    else:
        crt_row += "."
    if (cycle % 40) == 0:
        print(crt_row)
        crt_row = ""
        crt_row_cnt += 1
        if crt_row_cnt == 6:
            print("==============================================")
        score += reg_x * cycle


with open(Path(__file__).parent/"10.txt") as f:
    for line in f:
        do_cycle()
        line = line.strip()
        if line == "noop":
            continue
        # e.g. 'addx 5'
        do_cycle()
        delta_x = int(line[5:])
        reg_x += delta_x

print(f"Done: {score=}")
