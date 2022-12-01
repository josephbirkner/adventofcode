from pathlib import Path

calory_bags = [[]]
with open(Path(__file__).parent/"1.txt") as f:
    for cals in f:
        cals = cals.strip()
        if not cals:
            calory_bags.append([])
            continue
        calory_bags[-1].append(int(cals))

bag_sums = [sum(c for c in calories) for calories in calory_bags]
bag_sums.sort(reverse=True)
print(bag_sums[0] + bag_sums[1] + bag_sums[2])
