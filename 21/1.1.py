result = 0
with open("1.data", 'r') as f:
    prev_n = None
    for line in f:
        n = int(line.strip())
        if prev_n is None:
            prev_n = n
            continue
        if n > prev_n:
            result += 1
        prev_n = n
print(result)
