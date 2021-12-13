from collections import defaultdict

polymer = defaultdict(int)
rules = dict()

with open("14.data") as f:
    for line_number, line in enumerate(f):
        line = line.strip()
        if line_number == 0:
            for i in range(len(line)-1):
                at_end = i == len(line)-2
                polymer[(line[i:i+2], at_end)] += 1
        elif line:
            a, b = line.split(" -> ")
            assert a not in rules and len(a) == 2
            rules[a] = (a[0] + b, b + a[1])

for step in range(40):
    print(f"{step=}")
    new_poly = defaultdict(int)
    for (pair, at_end), count in polymer.items():
        if pair in rules:
            l, r = rules[pair]
            new_poly[(l, False)] += count
            new_poly[(r, at_end)] += count
        else:
            new_poly[(pair, at_end)] += count
    assert sum(1 for (x, y), z in new_poly.items() if y) == 1
    polymer = new_poly
    el_counts = defaultdict(int)
    for (el_pair, el_at_end), el_count in polymer.items():
        for el in (el_pair[:-1] if not el_at_end else el_pair):
            el_counts[el] += el_count
    el_counts = list(el_counts.items())
    el_counts.sort(key=lambda el: el[1])
    print(el_counts)
    print("score:", el_counts[-1][1] - el_counts[0][1])
