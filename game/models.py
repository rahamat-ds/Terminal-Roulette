from dataclasses import dataclass, field
from enum import Enum, auto


class Chamber(Enum):
    SAFE = auto()
    DANGER = auto()


class GameStatus(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class Action(Enum):
    SPIN = auto()
    SHOOT = auto()


class Target(Enum):
    SELF = auto()
    OPPONENT = auto()


class ShotResult(Enum):
    SAFE = auto()
    DANGER = auto()


@dataclass
class Player:
    name: str
    is_human: bool = True
    spin_available: bool = True
    alive: bool = True


@dataclass
class TurnResult:
    player: str
    action: Action
    target: Target | None = None
    shot_result: ShotResult | None = None
    eliminated_player: str | None = None
    message: str = ""


@dataclass
class GameState:
    players: list[Player]
    current_player_index: int = 0
    status: GameStatus = GameStatus.PLAYING
    turn_number: int = 1
    history: list[TurnResult] = field(default_factory=list)

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    @property
    def opponent(self) -> Player:
        return self.players[1 - self.current_player_index]

    def advance_turn(self) -> None:
        self.current_player_index = 1 - self.current_player_index
        self.turn_number += 1
