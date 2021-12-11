from collections import defaultdict

tunnels = defaultdict(list)
paths = []


with open("12.data") as f:
    for line in f:
        line = line.strip()
        if line:
            start, end = line.split("-")
        tunnels[end].append(start)
        tunnels[start].append(end)


def navigate(visited: list, small_cave_revisited=False):
    global tunnels, paths
    if visited[-1] == "end":
        paths.append(visited)
        return
    for adjacent_cave in tunnels[visited[-1]]:
        small_cave_revisited_new = small_cave_revisited
        if adjacent_cave.islower():
            if adjacent_cave in visited:
                if adjacent_cave not in {"start", "end"} and not small_cave_revisited:
                    small_cave_revisited_new = True
                else:
                    continue
        navigate(visited+[adjacent_cave], small_cave_revisited_new)


navigate(["start"])
for path in paths:
    print(path)
print(len(paths))
