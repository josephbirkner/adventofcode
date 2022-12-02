from pathlib import Path

ROCK = 1
PAPER = 2
SCISSORS = 3

winning = {
    (ROCK, SCISSORS),
    (SCISSORS, PAPER),
    (PAPER, ROCK)
}

translation = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

points = 0

with open(Path(__file__).parent/"2.txt") as f:
    for line in f:
        prompt, response = map(lambda s: translation[s], line.strip().split(" "))
        won = (response, prompt) in winning
        lost = (prompt, response) in winning
        if won:
            points += response + 6
        elif lost:
            points += response
        else:
            points += response + 3

print(points)
