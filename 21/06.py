from collections import defaultdict

fish = [0]*9
with open("06.data") as f:
    for age in map(int, f.read().split(",")):
        fish[age] += 1

for _ in range(256):
    new_fish = fish[0]
    fish = fish[1:] + [0]
    fish[8] += new_fish
    fish[6] += new_fish

print(sum(fish))
