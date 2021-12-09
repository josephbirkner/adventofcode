import math

with open("10.data") as f:
    lines = [line.strip() for line in f]

expect = {
    "{": "}",
    "[": "]",
    "(": ")",
    "<": ">"
}
illegal_score = {
    "}": 1197,
    "]": 57,
    ")": 3,
    ">": 25137
}
completion_score = {
    "}": 3,
    "]": 2,
    ")": 1,
    ">": 4
}
illegal_stops = []
good_lines = []

for line in lines:
    stack = []
    line_is_bad = False
    for character in line:
        if character in expect:
            stack.append(expect[character])
        elif stack[-1] == character:
            stack = stack[:-1]
        else:
            illegal_stops.append(character)
            print(f"Found illegal delimiter: {character}")
            line_is_bad = True
            break
    if not line_is_bad:
        print("Line is good.")
        stack.reverse()
        stack = ''.join(stack)
        print(f"Line {line} will be completed with {stack}.")
        good_lines.append(stack)

illegal_score_total = sum(illegal_score[c] for c in illegal_stops)
print(illegal_score_total)

score_per_line = []

for completion_sequence in good_lines:
    score = 0
    for character in completion_sequence:
        score *= 5
        score += completion_score[character]
    score_per_line.append(score)
    print(f"{completion_sequence}: {score=}")

score_per_line.sort()
print(score_per_line)
middle_index = math.floor(len(score_per_line)/2.)
print(f"Middle index of {len(score_per_line)} is {middle_index}")
print(score_per_line[middle_index])
