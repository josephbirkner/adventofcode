dots = set()
folds = []

with open("13.data") as f:
    for line in f:
        line = line.strip()
        if "," in line:
            x, y = line.split(",")
            dots.add((int(x), int(y)))
        elif line.startswith("fold along "):
            fold_axis, fold_coord = line[11:].split("=")
            folds.append((fold_axis, int(fold_coord)))

for fold_axis, fold_coord in folds:
    print(f"Folding along {fold_axis}={fold_coord}")
    new_dots = set()
    if fold_axis == "x":
        for x, y in dots:
            if x == fold_coord:
                continue
            if x > fold_coord:
                x = fold_coord - (x - fold_coord)
            new_dots.add((x, y))
            assert x >= 0
    elif fold_axis == "y":
        for x, y in dots:
            if y == fold_coord:
                continue
            if y > fold_coord:
                y = fold_coord - (y - fold_coord)
            new_dots.add((x, y))
            assert y >= 0
    print(f"{len(new_dots)=}")
    dots = new_dots


field_size = [max(x for x, _ in dots)+1, max(y for _, y in dots)+1]
field = [[" "]*field_size[0] for _ in range(field_size[1])]
for x, y in dots:
    field[y][x] = "#"
for line in field:
    print(''.join(line))
