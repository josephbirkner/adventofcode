from pathlib import Path


def range_within(r1s, r1e, r2s, r2e):
    assert r1s <= r1e and r2s <= r2e
    return r1s >= r2s and r1e <= r2e


def range_overlap(r1s, r1e, r2s, r2e):
    return (r2s <= r1s <= r2e) or (r2s <= r1e <= r2e)


ranges_within = 0
ranges_overlap = 0

with open(Path(__file__).parent/"4.txt") as f:
    for line in f:
        line = line.strip()
        r1, r2 = map(lambda rr: (int(rr[0]), int(rr[1])), map(lambda rs: rs.split("-"), line.split(",")))
        if range_within(*r1, *r2) or range_within(*r2, *r1):
            ranges_within += 1
            ranges_overlap += 1
        elif range_overlap(*r1, *r2):
            ranges_overlap += 1

print(ranges_within)
print(ranges_overlap)
