from pathlib import Path


def score(thing: str) -> int:
    if thing.isupper():
        return ord(thing) - ord('A') + 27
    else:
        return ord(thing) - ord('a') + 1


total = 0

with open(Path(__file__).parent/"3.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        bag1, bag2 = line[:len(line)//2], line[len(line)//2:]
        common_items = list(set(bag1) & set(bag2))
        assert len(common_items) == 1
        for item in common_items:
            total += score(item)

print(total)
