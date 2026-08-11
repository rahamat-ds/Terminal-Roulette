import random

from game.engine import GameEngine
from game.models import Player, GameStatus, ShotResult, Target
from game.revolver import Revolver


def make_engine():
    revolver = Revolver(rng=random.Random(10))
    return GameEngine(
        Player("Alice"),
        Player("Bob"),
        revolver=revolver,
    )


def test_spin_consumes_player_spin_and_turn():
    engine = make_engine()

    assert engine.state.current_player.name == "Alice"
    assert engine.state.current_player.spin_available is True

    engine.spin()

    assert engine.state.players[0].spin_available is False
    assert engine.state.current_player.name == "Bob"


def test_player_cannot_spin_twice():
    engine = make_engine()

    engine.spin()

    # Bob is now active; make Alice active again by a safe shot.
    engine.shoot(Target.OPPONENT)

    # Alice has already used her spin.
    try:
        engine.spin()
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_safe_shot_passes_turn():
    engine = make_engine()

    engine.revolver._chambers[engine.revolver.current_position] = engine.revolver._chambers[
        engine.revolver.current_position
    ]

    # Force current chamber to safe for deterministic testing.
    engine.revolver._chambers[engine.revolver.current_position] = next(
        c for c in engine.revolver._chambers
        if c.name == "SAFE"
    )

    result = engine.shoot(Target.OPPONENT)

    assert result.shot_result is ShotResult.SAFE
    assert engine.state.current_player.name == "Bob"


def test_danger_shot_ends_game_and_eliminates_target():
    engine = make_engine()
    target_index = engine.state.current_player_index
    target = engine.state.opponent
    engine.revolver.current_position = engine.revolver.danger_position()

    result = engine.shoot(Target.OPPONENT)

    assert result.shot_result is ShotResult.DANGER
    assert target.alive is False
    assert engine.state.status is GameStatus.GAME_OVER
