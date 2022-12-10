import itertools
from itertools import permutations
SYMBOLS = "abcdefg"

correct_patterns = [
    set("abcefg"),
    set("cf"),
    set("acdeg"),
    set("acdfg"),
    set("bdcf"),
    set("abdfg"),
    set("abdfeg"),
    set("acf"),
    set("abcdefg"),
    set("abcdfg")
]
wire_combinations = list(permutations(SYMBOLS))


def translate(pattern, wire_combination):
    tr_pattern = {wire_combination[ord(c)-ord('a')] for c in pattern}
    try:
        index = correct_patterns.index(tr_pattern)
        return index, tr_pattern
    except ValueError as e:
        return None


result = 0
with open("08.data") as f:
    for line in f:
        lhs, rhs = line.strip().split(" | ")
        patterns = lhs.split(" ")
        resolved = False
        for combination in wire_combinations:
            if any(translate(pat, combination) is None for pat in patterns):
                continue
            resolved = True
            break
        if not resolved:
            print(f"Failed! -> {line}")
            exit(1)
        number = 0
        for pat in rhs.split(" "):
            number *= 10
            digit, _ = translate(pat, combination)
            number += digit
        assert number >= 0
        result += number

print(result)
