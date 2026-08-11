# T E R M I N A L  R O U L E T T E

A two-player CLI game inspired by Russian Roulette.

🎮 
├── game engine
├── revolver mechanics
├── Human vs Human
├── Human vs Computer
├── CLI
└── tests

## Requirements

- Python 3.10+
- No third-party packages

## Run

From the project directory:

```bash
python main.py
```

On Linux/macOS, you can also use:

```bash
python3 main.py
```

## Test

The project uses Python's standard-library-compatible test layout, but the
test runner is easiest with pytest if you have it installed:

```bash
pytest
```

If you want to stay strictly standard-library-only:

```bash
python -m unittest
```

(The current tests use pytest-style assertions, so `pytest` is recommended
for development. The game itself has zero third-party dependencies.)

## Game rules

- A classic revolver with six chambers.
- Exactly one danger chamber.
- The cylinder is randomized at the beginning of every match.
- On a turn, a player may shoot or spin the barrel.
- Spinning randomizes the entire cylinder again and consumes the player's turn.
- After spinning, the gun passes directly to the opponent.
- Each player gets exactly one spin per match.
- Shooting allows targeting yourself or the opponent.
- Every trigger pull advances the cylinder one chamber.
- A safe shot passes the turn.
- A danger shot ends the match.
- There is no turn limit.

## Architecture

```text
main.py
   |
   v
cli/interface.py ----> cli/display.py
   |
   v
game/engine.py
   |
   +---- game/models.py
   |
   +---- game/revolver.py
```

The CLI handles input/output. The game engine handles rules. The revolver
handles cylinder state and randomness. This separation makes it possible to
add a stronger AI opponent, statistics/simulation mode, or 3–4 player mode later
without rewriting the core rules.
