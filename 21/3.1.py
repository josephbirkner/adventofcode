gamma = 0
epsilon = 0
lines = []

with open("3.data", 'r') as f:
    for line in f:
        l = line.strip()
        if l:
            assert not lines or len(lines[-1]) == len(l)
            lines.append(l)

for pos in range(len(lines[0])):
    counts = [0, 0]
    epsilon <<= 1
    gamma <<= 1
    for line in lines:
        counts[int(line[pos])] += 1
    if counts[0] > counts[1]:
        epsilon |= 1
    elif counts[1] > counts[0]:
        gamma |= 1
    else:
        # Tie!
        assert False

# epsilon : 010001011010 (1114)
# gamma   : 101110100101 (2981)
# product : 3320834
print(f"epsilon : {epsilon:b} ({epsilon})")
print(f"gamma   : {gamma:b} ({gamma})")
print(f"product : {epsilon*gamma}")
