import random

from game.engine import GameEngine
from game.models import Player, Target, GameStatus
from cli.display import (
    banner,
    clear,
    pause,
    show_history,
    show_result,
    show_rules,
    show_status,
)


def run() -> None:
    while True:
        clear()
        banner()
        print("1. Human vs Human")
        print("2. Human vs Computer")
        print("3. Rules")
        print("4. Quit")

        choice = input("\n> ").strip()

        if choice == "1":
            start_match(vs_computer=False)
        elif choice == "2":
            start_match(vs_computer=True)
        elif choice == "3":
            clear()
            banner()
            show_rules()
            input("\nPress Enter to return...")
        elif choice == "4":
            print("\nGoodbye.")
            return
        else:
            print("\nInvalid choice.")
            pause()


def start_match(vs_computer: bool) -> None:
    clear()
    banner()

    if vs_computer:
        human_name = input("Your name [Player 1]: ").strip() or "Player 1"
        player1 = Player(human_name, is_human=True)
        player2 = Player("Computer", is_human=False)
    else:
        name1 = input("Player 1 name [Player 1]: ").strip() or "Player 1"
        name2 = input("Player 2 name [Player 2]: ").strip() or "Player 2"
        player1 = Player(name1)
        player2 = Player(name2)

    engine = GameEngine(player1, player2)

    print("\nThe cylinder is loaded.")
    pause()
    game_loop(engine, vs_computer)


def game_loop(engine: GameEngine, vs_computer: bool) -> None:
    while engine.state.status is GameStatus.PLAYING:
        clear()
        banner()
        show_status(engine)

        player = engine.state.current_player

        if vs_computer and not player.is_human:
            computer_turn(engine)
        else:
            human_turn(engine)

    clear()
    banner()
    print("\nGAME OVER")
    print("---------")
    print(f"{engine.state.history[-1].message}")
    input("\nPress Enter to return to menu...")


def human_turn(engine: GameEngine) -> None:
    player = engine.state.current_player

    print(f"\n{player.name}'s turn.")

    while True:
        print("\nActions:")
        print("  [P]ull the trigger")
        if player.spin_available:
            print("  [S]pin the barrel (use your one spin)")
        print("  [H]istory")
        print("  [Q]uit match")

        choice = input("\n> ").strip().lower()

        if choice in {"p", "shoot"}:
            target = choose_target(engine)
            result = engine.shoot(target)
            show_result(result)
            if engine.state.status is GameStatus.PLAYING:
                input("\nPress Enter...")
            return

        if choice in {"s", "spin"} and player.spin_available:
            result = engine.spin()
            show_result(result)
            input("\nPress Enter...")
            return

        if choice in {"h", "history"}:
            show_history(engine)
            input("\nPress Enter...")
            continue

        if choice in {"q", "quit"}:
            engine.state.status = GameStatus.GAME_OVER
            return

        print("Invalid command.")


def choose_target(engine: GameEngine) -> Target:
    player = engine.state.current_player
    opponent = engine.state.opponent

    while True:
        print("\nTarget:")
        print(f"  [1] {player.name} (self)")
        print(f"  [2] {opponent.name}")
        choice = input("\n> ").strip().lower()

        if choice in {"1", "self", "me"}:
            return Target.SELF
        if choice in {"2", "opponent", "other"}:
            return Target.OPPONENT

        print("Invalid target.")


def computer_turn(engine: GameEngine) -> None:
    player = engine.state.current_player
    print(f"\n{player.name} is thinking...")
    pause(1.0)

    # The computer uses its spin when the current sequence has become
    # relatively dangerous, but only once. It does not inspect the
    # hidden chamber arrangement.
    safe_pulls_since_spin = count_safe_pulls_since_last_spin(engine)

    if player.spin_available and safe_pulls_since_spin >= 4:
        print("\nComputer chooses to spin.")
        pause()
        result = engine.spin()
        show_result(result)
        input("\nPress Enter...")
        return

    # In a rational two-player game, shooting the opponent dominates
    # shooting oneself. The computer therefore chooses the opponent.
    print(f"\nComputer targets {engine.state.opponent.name}.")
    pause(0.8)

    result = engine.shoot(Target.OPPONENT)
    show_result(result)

    if engine.state.status is GameStatus.PLAYING:
        input("\nPress Enter...")


def count_safe_pulls_since_last_spin(engine: GameEngine) -> int:
    count = 0

    for event in reversed(engine.state.history):
        if event.action.name == "SPIN":
            break
        if event.shot_result is not None and event.shot_result.name == "SAFE":
            count += 1

    return count
