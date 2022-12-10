from pathlib import Path


def score(thing: str) -> int:
    if thing.isupper():
        return ord(thing) - ord('A') + 27
    else:
        return ord(thing) - ord('a') + 1


total = 0

with open(Path(__file__).parent/"03.txt") as f:
    group_items = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        group_items.append(set(line))
        if len(group_items) == 3:
            common_items = (group_items[0] & group_items[1] & group_items[2])
            group_items.clear()
            assert len(common_items) == 1
            for item in common_items:
                total += score(item)

assert not group_items
print(total)
