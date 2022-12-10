from pathlib import Path
import numpy as np

forest = []

with open(Path(__file__).parent/"08.txt") as f:
    for line in f:
        forest.append(list(map(int, line.strip())))

forest = np.array(forest)
scores = np.zeros((4, *forest.shape))


def score_l2r(score_sheet: np.ndarray):
    for tree_line, score_line in zip(forest, score_sheet):
        visible_trees = []  # Currently tracked trees
        for i, tree_height in enumerate(tree_line):
            for scoring_tree, _ in visible_trees:
                score_line[scoring_tree] += 1
            # Forget trees which cannot look beyond this one
            visible_trees = [(j, h) for j, h in visible_trees if h > tree_height]
            visible_trees.append((i, tree_height))


# L2R
score_l2r(scores[0])

# R2L
orig_forest = forest.copy()
forest = np.flip(forest, axis=1)
scores = np.flip(scores, axis=2)
score_l2r(scores[1])

# T2B
forest = np.flip(forest, axis=1)
scores = np.flip(scores, axis=2)
forest = forest.transpose()
scores = scores.transpose((0, 2, 1))
score_l2r(scores[2])

# B2T
forest = np.flip(forest, axis=1)
scores = np.flip(scores, axis=2)
score_l2r(scores[3])

scores = scores.transpose((1, 2, 0))
scores = np.prod(scores, axis=2)

print(f"Highest score: {np.max(scores)}")
