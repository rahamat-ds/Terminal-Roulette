import random

from game.models import Chamber, ShotResult


class Revolver:
    """
    Six-chamber game revolver.

    There is always exactly one danger chamber.
    A spin randomizes the complete chamber arrangement and the
    chamber currently aligned with the barrel.
    """

    def __init__(self, capacity: int = 6, rng: random.Random | None = None):
        if capacity < 2:
            raise ValueError("A revolver needs at least two chambers.")

        self.capacity = capacity
        self.rng = rng or random.Random()
        self._chambers: list[Chamber] = []
        self.current_position = 0
        self.reload()

    def reload(self) -> None:
        self._chambers = [Chamber.SAFE] * self.capacity
        danger_index = self.rng.randrange(self.capacity)
        self._chambers[danger_index] = Chamber.DANGER
        self.current_position = self.rng.randrange(self.capacity)

    def spin(self) -> None:
        """
        Randomize the complete cylinder arrangement and select a
        random chamber to align with the barrel.
        """
        self.rng.shuffle(self._chambers)
        self.current_position = self.rng.randrange(self.capacity)

    def pull(self) -> ShotResult:
        result = (
            ShotResult.DANGER
            if self._chambers[self.current_position] is Chamber.DANGER
            else ShotResult.SAFE
        )

        self.current_position = (self.current_position + 1) % self.capacity
        return result

    def danger_position(self) -> int:
        """Used only by tests/debugging; the CLI never exposes this."""
        return self._chambers.index(Chamber.DANGER)

    def chamber_at_current_position(self) -> Chamber:
        """Used only by tests/debugging."""
        return self._chambers[self.current_position]
