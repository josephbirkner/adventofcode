import re

with open("04.data") as f:
    lines = f.readlines()
    numbers = list(map(int, lines[0].split(",")))
    lines = lines[2:]
    boards = []
    next_board = []
    for line in lines:
        line = line.strip()
        if not line:
            assert len(next_board) == 0
            continue
        board_line_numbers = list(map(int, re.compile(r"\s+").split(line)))
        next_board.append(board_line_numbers)
        if len(next_board) == 5:
            boards.append(next_board)
            next_board = []

print("numbers:", numbers)
print("boards:", boards)

won_boards = set()
for number in numbers:
    print("next number:", number)
    # mark all boards which have the number with -1
    for board_id, board in enumerate(boards):
        if board_id in won_boards:
            continue
        for line in board:
            for i in range(len(line)):
                if line[i] == number:
                    line[i] = -1
                    if all(map(lambda n: n == -1, line)) or all(map(lambda n: n == -1, (l[i] for l in board))):
                        print(f"board won:", board)
                        print(f"score numbers:", [n for line in board for n in line if n >= 0])
                        score = sum(n for line in board for n in line if n >= 0)
                        score *= number
                        print("final score:", score)
                        won_boards.add(board_id)
