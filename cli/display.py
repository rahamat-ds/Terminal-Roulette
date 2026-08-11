import os
import time

from game.models import ShotResult


TITLE = r"""
╔═══════════════════════════╗
║                           ║
║      T E R M I N A L      ║
║      R O U L E T T E      ║            
║                           ║
╚═══════════════════════════╝
"""


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def banner() -> None:
    print(TITLE)


def pause(seconds: float = 0.7) -> None:
    time.sleep(seconds)


def show_rules() -> None:
    print(
        """
RULES
-----

• The cylinder has 6 chambers and exactly 1 danger chamber.
• The danger chamber is randomized at the start of every match.
• On your turn, choose to SHOOT or SPIN.
• If you SPIN, the whole cylinder is randomized again.
• Each player may SPIN exactly once per match.
• Spinning consumes your entire turn and immediately passes the gun
  to your opponent.
• If you SHOOT, choose yourself or your opponent as the target.
• After every trigger pull, the cylinder advances by one chamber.
• A safe pull passes the turn to the other player.
• A danger pull ends the match immediately.

There is no turn limit. The match ends only when someone is hit.
"""
    )




def show_result(result) -> None:
    if result.action.name == "SPIN":
        print(f"\n{result.player} spins the cylinder...")
        pause()
        print(f"* {result.player} hands the gun to the opponent. *")
        return

    if result.target.name == "SELF":
        print(f"\n{result.player} points the gun at themselves.")
    else:
        print(f"\n{result.player} points the gun at the opponent.")

    print(f"{result.player} pulls the trigger...")
    pause(0.9)

    if result.shot_result is ShotResult.SAFE:
        print("\nCLICK.")
    else:
        print("\nBANG.")

    pause(0.7)
    print(result.message)


def show_status(engine) -> None:
    state = engine.state
    print("\nSTATUS")
    print("------")
    print(f"Turn: {state.turn_number}")
    print(f"Current player: {state.current_player.name}")

    for player in state.players:
        spin = "AVAILABLE" if player.spin_available else "USED"
        print(f"{player.name}: spin {spin}")


def show_history(engine) -> None:
    print("\nHISTORY")
    print("-------")

    if not engine.state.history:
        print("No actions yet.")
        return

    for index, event in enumerate(engine.state.history, start=1):
        if event.action.name == "SPIN":
            print(f"{index:>2}. {event.player} — SPIN")
        else:
            target = (
                "self" if event.target.name == "SELF"
                else engine.state.opponent.name
            )
            result = event.shot_result.name
            print(f"{index:>2}. {event.player} — SHOOT {target} — {result}")
