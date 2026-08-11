import random

from game.models import Chamber, ShotResult
from game.revolver import Revolver


def test_revolver_has_exactly_one_danger_chamber():
    revolver = Revolver(rng=random.Random(1))

    danger_count = sum(
        chamber is Chamber.DANGER
        for chamber in revolver._chambers
    )

    assert danger_count == 1


def test_pull_advances_position():
    revolver = Revolver(rng=random.Random(2))
    start = revolver.current_position

    revolver.pull()

    assert revolver.current_position == (start + 1) % revolver.capacity


def test_spin_changes_current_position_or_arrangement():
    revolver = Revolver(rng=random.Random(3))
    before = list(revolver._chambers)
    before_position = revolver.current_position

    revolver.spin()

    after = list(revolver._chambers)
    after_position = revolver.current_position

    assert sum(c is Chamber.DANGER for c in after) == 1
    assert sorted(c.name for c in before) == sorted(c.name for c in after)
    assert (before != after) or (before_position != after_position)


def test_danger_shot_returns_danger():
    revolver = Revolver(rng=random.Random(4))
    revolver.current_position = revolver.danger_position()

    assert revolver.pull() is ShotResult.DANGER
