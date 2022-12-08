from pathlib import Path
import numpy as np

forest = []

with open(Path(__file__).parent/"8.txt") as f:
    for line in f:
        forest.append(list(map(int, line.strip())))

forest = np.array(forest)
visible = np.zeros(forest.shape, dtype=bool)


def check_visibility_l2r():
    for tree_line, visibility_line in zip(forest, visible):
        last_height = -1
        for i, tree_height in enumerate(tree_line):
            if tree_height > last_height:
                visibility_line[i] = True
                last_height = tree_height


# L2R
check_visibility_l2r()

# R2L
orig_forest = forest.copy()
forest = np.flip(forest, axis=1)
visible = np.flip(visible, axis=1)
check_visibility_l2r()

# T2B
forest = np.flip(forest, axis=1)
visible = np.flip(visible, axis=1)
forest = forest.transpose()
visible = visible.transpose()
check_visibility_l2r()

# B2T
forest = np.flip(forest, axis=1)
visible = np.flip(visible, axis=1)
check_visibility_l2r()

visible = np.flip(visible, axis=1).transpose()
forest = np.flip(forest, axis=1).transpose()


print(f"Visible trees: {np.sum(visible.astype(int))}")
