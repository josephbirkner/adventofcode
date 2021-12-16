from matplotlib import pyplot as plt

with open("17.data") as f:
    x_range, y_range = f.read()[13:].split(", ")
    x_range = list(map(int, x_range[2:].split("..")))
    y_range = list(map(int, y_range[2:].split("..")))
    x_range.sort()
    y_range.sort()

print(x_range, y_range)

global lines


def plot_trajectory(vx, vy):
    x, y = 0, 0
    xarr, yarr = [0], [0]
    y_max = 0
    hit = False
    while y > y_range[0] and x < x_range[1]:
        x += vx
        y += vy
        y_max = max(y, y_max)
        vx = vx - 1 if vx > 0 else (vx + 1 if vx < 0 else 0)
        vy = vy - 1
        xarr.append(x)
        yarr.append(y)
        if x_range[0] <= x <= x_range[1]:
            if y_range[0] <= y <= y_range[1]:
                hit = True
                break
    if hit:
        plt.plot(xarr, yarr)
    return hit, y_max


hits = 0

working_vx = []
working_vy = []

for vx_ in range(x_range[1] + 1000):
    for vy_ in range(y_range[0] - 1000, 1000):
        h, _ = plot_trajectory(vx_, vy_)
        if h:
            hits += 1
            working_vy.append(vy_)
            working_vx.append(vx_)
print("hits:", hits)

# print(min(working_vx), max(working_vx))
# print(min(working_vy), max(working_vy))

plt.plot(
    [x_range[0], x_range[1],
     x_range[0], x_range[1],
     x_range[0]],
    [y_range[1], y_range[0],
     y_range[0], y_range[1],
     y_range[1]])
plt.show()

for vx_, vy_ in zip(working_vx, working_vy):
    print(f"{vx_},{vy_}")
