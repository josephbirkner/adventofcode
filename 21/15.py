from copy import deepcopy

MAX_RISK = 999999999999999999999999999

field = []
risk_field = []
best_path_risk = MAX_RISK

with open("15.data") as f:
    for line in f:
        line = list(map(int, line.strip()))
        field.append(line+[0]*len(line)*4)
        risk_field.append([MAX_RISK] * len(line) * 5)
for i in range(len(field) * 4):
    risk_field.append([MAX_RISK] * len(line) * 5)
    field.append([0] * len(line) * 5)
tile_size_x, tile_size_y = len(field[0])//5, len(field)//5
print(f"{tile_size_x=}")
print(f"{tile_size_y=}")

for field_x in range(0, 5):
    for field_y in range(0, 5):
        increment = field_x + field_y
        for y in range(tile_size_y):
            for x in range(tile_size_x):
                xx = field_x * tile_size_x + x
                yy = field_y * tile_size_y + y
                field[yy][xx] = field[y][x]
                for i in range(increment):
                    field[yy][xx] += 1
                    if field[yy][xx] > 9:
                        field[yy][xx] = 1

for line in field:
    print(" ".join(str(x) for x in line))

goal_pos = (len(field[0])-1, len(field)-1)
goal_x, goal_y = goal_pos
risk_field[goal_y][goal_x] = field[goal_y][goal_x]

step = 0
while True:
    step += 1
    print(f"Iteration {step}")
    changed = False
    for y, row in enumerate(risk_field):
        for x, path_risk in enumerate(row):
            for nb_x, nb_y in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if nb_x >= len(row) or nb_x < 0:
                    continue
                if nb_y >= len(risk_field) or nb_y < 0:
                    continue
                alt_risk = field[y][x] + risk_field[nb_y][nb_x]
                if alt_risk < path_risk:
                    risk_field[y][x] = alt_risk
                    changed = True
    if not changed:
        break

print(risk_field[0][0] - field[0][0])
