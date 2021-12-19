enhancement = ""
image = set()
image_height = 0
padding_bit = 0


def extents(padding=0):
    global image
    min_x = min(x for x, _ in image)
    max_x = max(x for x, _ in image)
    min_y = min(y for _, y in image)
    max_y = max(y for _, y in image)
    return (
        range(min_x-padding, max_x+1+padding),
        range(min_y-padding, max_y+1+padding))


def coords_around(x_, y_):
    yield x_ - 1, y_ - 1
    yield x_, y_ - 1
    yield x_ + 1, y_ - 1
    yield x_ - 1, y_
    yield x_, y_
    yield x_ + 1, y_
    yield x_ - 1, y_ + 1
    yield x_, y_ + 1
    yield x_ + 1, y_ + 1


with open("20.data") as f:
    enhancement_parsed = False
    for line in f:
        line = line.strip()
        if not line and not enhancement_parsed:
            enhancement_parsed = True
        elif not enhancement_parsed:
            enhancement += line
        else:
            for x_coord, character in enumerate(line):
                if character == "#":
                    image.add((x_coord, image_height))
            image_height += 1


def enhance():
    global image, padding_bit
    new_image = set()
    x_range, y_range = extents()
    x_range_padded, y_range_padded = extents(1)
    for x in x_range_padded:
        for y in y_range_padded:
            lookup_index = 0
            for coords in coords_around(x, y):
                lookup_index <<= 1
                if (coords[0] not in x_range) or (coords[1] not in y_range):
                    lookup_index |= padding_bit
                elif coords in image:
                    lookup_index |= 1
            enhancement_info = enhancement[lookup_index]
            if enhancement_info == "#":
                new_image.add((x, y))
    image = new_image
    padding_bit = 1 - padding_bit
    print(f"enhancement done: image now has {len(image)} lit pixels.")


def paint():
    print()
    x_range, y_range = extents()
    for y in y_range:
        print("".join([".", "#"][(x, y) in image] for x in x_range))
    print()


assert len(enhancement) == 512
for _ in range(50):
    enhance()
