result = 0
with open("01.data", 'r') as f:
    window = []
    prev_sum = None
    for line in f:
        n = int(line.strip())
        if len(window) > 2:
            window = window[1:]
        window.append(n)
        if len(window) > 2:
            new_sum = sum(window)
            if prev_sum is not None:
                if new_sum > prev_sum:
                    result += 1
            prev_sum = new_sum
print(result)
