import random
import time
import json
import os
from typing import Dict, Optional, Tuple

HIGHSCORE_FILE = "high_scores.json"

difficulties = {1: {"name": "Easy", "chances": 10},
                2: {"name": "Medium", "chances": 5},
                3: {"name": "Hard", "chances": 3}
}


def load_high_scores() -> Dict[str, Optional[int]]:
    if not os.path.exists(HIGHSCORE_FILE):
        return {info["name"]: None for info in difficulties.values()}
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure all difficulties exist in file
        for info in difficulties.values():
            data.setdefault(info["name"], None)
        return data
    except (json.JSONDecodeError, OSError):
        return {info["name"]: None for info in difficulties.values()}


def save_high_scores(scores: Dict[str, Optional[int]]) -> None:
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError:
        pass


def next_hint(
    number: int,
    min_possible: int,
    max_possible: int,
    provided_hints: set
) -> Tuple[str, set]:
    # We provide a different hint each time, cycling through categories.
    # 1) Range narrowing
    if "range" not in provided_hints:
        provided_hints.add("range")
        lower = max(1, min_possible)
        upper = min(100, max_possible)
        return f"Hint: The number is between {lower} and {upper}.", provided_hints

    # 2) Parity
    if "parity" not in provided_hints:
        provided_hints.add("parity")
        parity = "even" if number % 2 == 0 else "odd"
        return f"Hint: The number is {parity}.", provided_hints

    # 3) Divisibility (choose a relevant small prime or 5 if applicable)
    if "div" not in provided_hints:
        provided_hints.add("div")
        for d in (3, 5, 7):
            if number % d == 0:
                return f"Hint: The number is divisible by {d}.", provided_hints
        return "Hint: The number is not divisible by 3, 5, or 7.", provided_hints

    # 4) Proximity bucket (broad hot/cold)
    if "proximity" not in provided_hints:
        provided_hints.add("proximity")
        # Provide a generic proximity hint; actual distance depends on latest guess,
        # but since we don't know it here, give a coarse band based on the range size.
        span = max_possible - min_possible
        if span <= 10:
            return "Hint: You are very close (tight range)!", provided_hints
        elif span <= 20:
            return "Hint: You are getting warmer (moderate range).", provided_hints
        else:
            return "Hint: Still quite broad; try splitting the range.", provided_hints

    # If all hints given, repeat range (it will still be useful)
    lower = max(1, min_possible)
    upper = min(100, max_possible)
    return f"Hint: The number is between {lower} and {upper}.", provided_hints


def game(max_attempts: int, difficulty_name: str, high_scores: Dict[str, Optional[int]]) -> Optional[int]:
    number = random.randint(1, 100)
    attempts = 0
    min_possible = 1
    max_possible = 100
    provided_hints: set = set()
    last_guess: Optional[int] = None

    print(f"\nGuess the number (1-100). You have {max_attempts} attempts.")
    print("Type 'hint' for a clue (costs 1 attempt), or 'quit' to end the round.")

    start_time = time.time()

    while attempts < max_attempts:
        raw = input(f"Attempt {attempts + 1}/{max_attempts} - Enter your guess: ").strip().lower()

        if raw == "quit":
            print("Round ended. Better luck next time!")
            return None

        if raw == "hint":
            attempts += 1
            hint, provided_hints = next_hint(number, min_possible, max_possible, provided_hints)
            print(hint)
            remaining = max_attempts - attempts
            print(f"(Hint used. Attempts remaining: {remaining})")
            continue

        try:
            guess = int(raw)
        except ValueError:
            print("Please enter a valid number, 'hint', or 'quit'.")
            continue

        if not (1 <= guess <= 100):
            print("Your guess must be between 1 and 100.")
            continue

        attempts += 1
        last_guess = guess

        if guess == number:
            elapsed = time.time() - start_time
            print(f"Congratulations! You guessed the number in {attempts} attempts and {elapsed:.2f} seconds!")
            # High score update (fewest attempts)
            best = high_scores.get(difficulty_name)
            if best is None or attempts < best:
                high_scores[difficulty_name] = attempts
                save_high_scores(high_scores)
                print(f"New high score for {difficulty_name}: {attempts} attempts!")
            else:
                print(f"High score for {difficulty_name} remains: {best} attempts.")
            return attempts

        # Update range bounds based on guess
        if guess < number:
            print(f"Incorrect! The number is greater than {guess}.")
            min_possible = max(min_possible, guess + 1)
        else:
            print(f"Incorrect! The number is less than {guess}.")
            max_possible = min(max_possible, guess - 1)

        # Proximity feedback
        distance = abs(number - guess)
        if distance <= 5:
            print("You're very hot (within 5)!")
        elif distance <= 10:
            print("You're warm (within 10).")
        elif distance <= 20:
            print("You're cool (within 20).")
        else:
            print("You're cold (more than 20 away).")

        # Auto-hint when low on attempts and hints still available
        remaining = max_attempts - attempts
        if remaining in (2, 1) and len(provided_hints) < 4:
            auto_hint, provided_hints = next_hint(number, min_possible, max_possible, provided_hints)
            print(f"Auto-hint: {auto_hint} (no attempt cost)")

    print(f"Out of attempts! The number was {number}.")
    return None


def main():
    high_scores = load_high_scores()

    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("Please select the difficulty level:")

    for num, info in difficulties.items():
        best = high_scores.get(info['name'])
        hs_text = f" | High score: {best} attempts" if best is not None else ""
        print(f"{num}. {info['name']} ({info['chances']} chances){hs_text}")

    while True:
        try:
            user_choice = int(input("Enter your choice: "))
            if user_choice in difficulties:
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

    user_difficulty = difficulties[user_choice]
    difficulty_name = user_difficulty['name']
    print(f"Great! You have selected the {difficulty_name} difficulty level")
    print("Let's start the game!")

    max_attempts = user_difficulty['chances']
    while True:
        result = game(max_attempts, difficulty_name, high_scores)
        current_best = high_scores.get(difficulty_name)
        if current_best is None:
            print(f"Current high score for {difficulty_name}: {current_best} attempts")
        again = input("Do you want to play again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thank you for playing!")
            break

if __name__ == '__main__':
    main()