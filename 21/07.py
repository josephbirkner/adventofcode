with open("07.data") as f:
    crabs = list(map(int, f.read().split(",")))

max_pos = max(crabs)
min_pos = min(crabs)
avg_pos = int(sum(crabs)/len(crabs))

print(f"{max_pos=}, {min_pos=}, {avg_pos=}")
print("----------------------")
smallest_cost = None
while min_pos <= max_pos:
    cost = sum((abs(c-min_pos)*abs(c-min_pos)+abs(c-min_pos))/2 for c in crabs)
    print(f"cost at pos={min_pos}: {cost}")
    if smallest_cost is None or smallest_cost[0] > cost:
        smallest_cost = (cost, min_pos)
    min_pos += 1

print(f"Smallest cost: cost={smallest_cost[0]} pos={smallest_cost[1]}")
