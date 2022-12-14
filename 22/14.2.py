from pathlib import Path
from typing import Set, Tuple
from numpy import sign

occupied: Set[Tuple[int, int]] = set()

# Parse boulder locations
with open(Path(__file__).parent/"14.txt") as f:
    for line in f:
        line = line.strip()
        coord_pairs = line.split(" -> ")
        start_x, start_y = tuple(map(int, coord_pairs[0].split(",")))
        for coord_pair in coord_pairs[1:]:
            next_x, next_y = tuple(map(int, coord_pair.split(",")))
            dx = next_x - start_x
            dy = next_y - start_y
            if dx:
                for x in range(start_x, next_x + sign(dx), sign(dx)):
                    occupied.add((x, start_y))
            else:
                assert dy
                for y in range(start_y, next_y + sign(dy), sign(dy)):
                    occupied.add((start_x, y))
            start_x, start_y = next_x, next_y

# Find highest y coord
max_boulder_y = max(y for _, y in occupied)


def is_occupied(x_, y_):
    return y_ == max_boulder_y + 2 or (x_, y_) in occupied


# Add sand
grains = 0
while True:
    print("Next grain...")
    fell_into_space = False
    grain_x, grain_y = 500, 0
    # Fall...
    while True:
        grain_y += 1
        if not is_occupied(grain_x, grain_y):
            # Part 1
            # if grain_y > max_boulder_y:
            #     fell_into_space = True
            #     break
            continue
        if not is_occupied(grain_x-1, grain_y):
            grain_x -= 1
            continue
        if not is_occupied(grain_x+1, grain_y):
            grain_x += 1
            continue
        # Come to rest
        grain_y -= 1
        occupied.add((grain_x, grain_y))
        break
    if fell_into_space:
        break
    grains += 1
    if is_occupied(500, 0):
        break

print(f"Sand grains: {grains}")
