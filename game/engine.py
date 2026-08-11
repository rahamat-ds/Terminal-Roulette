from game.models import (
    Action,
    GameState,
    GameStatus,
    Player,
    ShotResult,
    Target,
    TurnResult,
)
from game.revolver import Revolver


class GameEngine:
    def __init__(self, player1: Player, player2: Player, revolver: Revolver | None = None):
        self.revolver = revolver or Revolver()
        self.state = GameState(players=[player1, player2])

    def spin(self) -> TurnResult:
        player = self.state.current_player

        if not player.spin_available:
            raise ValueError(f"{player.name} has already used their spin.")

        self.revolver.spin()
        player.spin_available = False

        result = TurnResult(
            player=player.name,
            action=Action.SPIN,
            message=f"{player.name} spun the cylinder and forfeited the turn.",
        )
        self.state.history.append(result)
        self.state.advance_turn()
        return result

    def shoot(self, target: Target) -> TurnResult:
        player = self.state.current_player
        target_player = player if target is Target.SELF else self.state.opponent

        shot_result = self.revolver.pull()

        if shot_result is ShotResult.DANGER:
            target_player.alive = False
            self.state.status = GameStatus.GAME_OVER
            message = f"{target_player.name} was hit."
        else:
            message = f"{target_player.name} survived."

        result = TurnResult(
            player=player.name,
            action=Action.SHOOT,
            target=target,
            shot_result=shot_result,
            eliminated_player=(
                target_player.name if shot_result is ShotResult.DANGER else None
            ),
            message=message,
        )
        self.state.history.append(result)

        if shot_result is ShotResult.SAFE:
            self.state.advance_turn()

        return result

    def reset(self) -> None:
        for player in self.state.players:
            player.spin_available = True
            player.alive = True

        self.revolver.reload()
        self.state.current_player_index = 0
        self.state.status = GameStatus.PLAYING
        self.state.turn_number = 1
        self.state.history.clear()
