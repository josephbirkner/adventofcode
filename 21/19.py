import numpy as np
from scipy.spatial.transform import Rotation as R

ROTATIONS = [
    R.from_euler("yxz", [0., 0., 0.], True),
    R.from_euler("yxz", [0., 0., 90.], True),
    R.from_euler("yxz", [0., 0., 180.], True),
    R.from_euler("yxz", [0., 0., 270.], True),
    R.from_euler("yxz", [0., -90., 0.], True),
    R.from_euler("yxz", [0., -90., 90.], True),
    R.from_euler("yxz", [0., -90., 180.], True),
    R.from_euler("yxz", [0., -90., 270.], True),
    R.from_euler("yxz", [0., 90., 0.], True),
    R.from_euler("yxz", [0., 90., 90.], True),
    R.from_euler("yxz", [0., 90., 180.], True),
    R.from_euler("yxz", [0., 90., 270.], True),
    R.from_euler("yxz", [90., 0., 0.], True),
    R.from_euler("yxz", [90., 0., 90.], True),
    R.from_euler("yxz", [90., 0., 180.], True),
    R.from_euler("yxz", [90., 0., 270.], True),
    R.from_euler("yxz", [180., 0., 0.], True),
    R.from_euler("yxz", [180., 0., 90.], True),
    R.from_euler("yxz", [180., 0., 180.], True),
    R.from_euler("yxz", [180., 0., 270.], True),
    R.from_euler("yxz", [270., 0., 0.], True),
    R.from_euler("yxz", [270., 0., 90.], True),
    R.from_euler("yxz", [270., 0., 180.], True),
    R.from_euler("yxz", [270., 0., 270.], True)
]

added_points = set()
added_sentries = set()
added_sentry_positions = []
sentry_points = []

with open("19.data") as f:
    for line in f:
        line = line.strip()
        if line:
            if line.startswith("--- "):
                sentry_points.append([])
            else:
                sentry_points[-1].append(
                    np.array(list(map(int, line.split(",")))))

print(f"mapping {len(sentry_points)} sentries ...")


def transform(points: list, rotation: int, offset: np.ndarray) -> set:
    return set(
        tuple(map(round, p))
        for p in (ROTATIONS[rotation].apply(points) + offset))


def transform_and_add(
        sentry_id: int,
        offset: np.ndarray,
        rotation: int):
    points = transform(sentry_points[sentry_id], rotation, offset)
    added_points.update(points)
    added_sentries.add(sentry_id)
    added_sentry_positions.append(offset)


def correlate(sentry_id: int) -> bool:
    my_points = sentry_points[sentry_id]
    # go through orientations
    for rotation in range(len(ROTATIONS)):
        my_points_rotated = transform(my_points, rotation, np.zeros(3))
        # go through my points
        for my_point in my_points_rotated:
            # go through other points
            for other_point in added_points:
                # derive translation as (other_point - my_point)
                translation = np.array(other_point) - my_point
                # apply translation to all points
                my_points_rotated_and_translated = set(
                    tuple(translation + p) for p in my_points_rotated)
                # check if at least 12 of them are known
                overlap = added_points & my_points_rotated_and_translated
                # print(f"{sentry_id}: {rotation=}, {translation=}, {len(overlap)=}")
                if len(overlap) >= 12:
                    print(f"{sentry_id}: successfully mapped!")
                    transform_and_add(sentry_id, translation, rotation)
                    return True
    return False


transform_and_add(0, np.zeros(3), 0)
while len(added_sentries) < len(sentry_points):
    changed = False
    for sid, _ in enumerate(sentry_points):
        if sid not in added_sentries:
            if correlate(sentry_id=sid):
                changed = True
    if not changed:
        print("stalled.")
        break
print(f"number of unique points: {len(added_points)}")

# find maximum manhattan distance
max_dist = 0
for s0 in added_sentry_positions:
    for s1 in added_sentry_positions:
        ds = s0 - s1
        max_dist = max(
            max_dist,
            sum(abs(x) for x in ds))
print(f"largest distance is {max_dist}")
