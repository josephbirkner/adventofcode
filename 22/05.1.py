from pathlib import Path

num_stacks = 9
stacks = [[] for _ in range(num_stacks)]
stacks_parsed = False
movement_instrs = []


with open(Path(__file__).parent/"05.txt") as f:
    for line in f:
        line = line.rstrip()

        if not line:
            if not stacks_parsed:
                stacks_parsed = True
            continue

        if not stacks_parsed:
            for i in range(num_stacks):
                n = 1+i*4
                if n >= len(line):
                    continue
                entry = line[n]
                if entry != " ":
                    stacks[i].append(entry)
        else:  # move x from y to z
            x, yz = line[5:].split(" from ")
            y, z = yz.split(" to ")
            movement_instrs.append((int(x), int(y), int(z)))

# reverse stacks, so the newest entry is always at the end
for stack in stacks:
    stack.reverse()

print(stacks)
print(movement_instrs)

for num, src, dst in movement_instrs:
    while num > 0:
        x = stacks[src-1].pop()
        stacks[dst-1].append(x)
        num -= 1


print("".join(s[-1] for s in stacks))
