cephalopods = []

with open("11.data") as f:
    for line in f:
        cephalopods.append(list(map(int, line.strip())))

flashes = 0


def increase(x_, y_, flashed_: set):
    global flashes
    if y_ >= len(cephalopods) or x_ >= len(cephalopods[y_]) or x_ < 0 or y_ < 0:
        return
    cephalopods[y_][x_] += 1
    if cephalopods[y_][x_] > 9 and (x_, y_) not in flashed_:
        flashes += 1
        flashed_.add((x_, y_))
        increase(x_ + 1, y_ + 1, flashed_)
        increase(x_ + 1, y_ - 1, flashed_)
        increase(x_ + 1, y_, flashed_)
        increase(x_ - 1, y_ + 1, flashed_)
        increase(x_ - 1, y_ - 1, flashed_)
        increase(x_ - 1, y_, flashed_)
        increase(x_, y_ + 1, flashed_)
        increase(x_, y_ - 1, flashed_)


step = 1
while True:
    # Advance energy levels
    flashed = set()
    for y, row in enumerate(cephalopods):
        for x, col in enumerate(row):
            increase(x, y, flashed)
    for x, y in flashed:
        cephalopods[y][x] = 0
    if len(flashed) == 100:
        print(f"They're on fire! {step=}")
        break
    step += 1

print(flashes)
