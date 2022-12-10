from pathlib import Path


ROCK = 1
PAPER = 2
SCISSORS = 3
WIN = 1
DRAW = 2
LOSE = 3

response_table = {
    (ROCK, WIN): PAPER,
    (ROCK, LOSE): SCISSORS,
    (ROCK, DRAW): ROCK,
    (SCISSORS, WIN): ROCK,
    (SCISSORS, LOSE): PAPER,
    (SCISSORS, DRAW): SCISSORS,
    (PAPER, WIN): SCISSORS,
    (PAPER, LOSE): ROCK,
    (PAPER, DRAW): PAPER,
}

translation = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": LOSE,
    "Y": DRAW,
    "Z": WIN
}

points = 0

with open(Path(__file__).parent/"02.txt") as f:
    for line in f:
        prompt, strategy = map(lambda s: translation[s], line.strip().split(" "))
        response = response_table[(prompt, strategy)]
        if strategy == WIN:
            points += response + 6
        elif strategy == LOSE:
            points += response
        else:
            assert strategy == DRAW
            points += response + 3

print(points)
