# Number Guessing Game (CLI, Python)

A simple, dependency-free command-line number guessing game (https://roadmap.sh/projects/number-guessing-game).  
The computer picks a random number **1–100**, and you try to guess it within a limited number of attempts.  
This version includes **difficulty levels**, a **hint system**, **proximity feedback**, **a timer**, and **per-difficulty high scores** saved to disk.

---

## Features

- **Three difficulties**: Easy (10 chances), Medium (5), Hard (3)
- **Hints** on demand (`hint`) that narrow the range, reveal parity, divisibility, or give proximity guidance
- **Auto-hints** when you’re almost out of attempts (no attempt cost)
- **Proximity feedback** after each wrong guess: *very hot / warm / cool / cold*
- **Timer** showing how long it took to guess correctly
- **High scores per difficulty** (fewest attempts), saved in `high_scores.json`
- **Quit anytime** during a round with `quit`

---

## Requirements

- **Python 3.8+**
- No third-party libraries required

---

## Setup & Run

Save the script as `number_guess.py` (or any filename you prefer) and run:

```bash
python number_guess.py
```

> If you use a different filename, replace it in the command above.

---

## How to Play

1. Pick a **difficulty** when prompted. This decides your maximum attempts.
2. Enter guesses (numbers **1–100**).
3. Use special commands:
   - Type `hint` to receive a clue (**costs 1 attempt**).
   - Type `quit` to abandon the current round.
4. The game ends when you guess the number or run out of attempts.
5. After a round, choose whether to **play again**.

### Difficulty Levels

| # | Name   | Chances |
|---|--------|---------|
| 1 | Easy   | 10      |
| 2 | Medium | 5       |
| 3 | Hard   | 3       |

---

## Sample Session

```
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
Please select the difficulty level:
1. Easy (10 chances)
2. Medium (5 chances)
3. Hard (3 chances)
Enter your choice: 2

Great! You have selected the Medium difficulty level
Let's start the game!

Guess the number (1-100). You have 5 attempts.
Type 'hint' for a clue (costs 1 attempt), or 'quit' to end the round.

Attempt 1/5 - Enter your guess: 50
Incorrect! The number is less than 50.
You're cool (within 20).

Attempt 2/5 - Enter your guess: 25
Incorrect! The number is greater than 25.
You're cool (within 20).

Attempt 3/5 - Enter your guess: hint
Hint: The number is between 26 and 49.
(Hint used. Attempts remaining: 2)

Attempt 4/5 - Enter your guess: 35
Incorrect! The number is less than 35.
You're warm (within 10).

Attempt 5/5 - Enter your guess: 30
Congratulations! You guessed the number in 5 attempts and 12.31 seconds!
New high score for Medium: 5 attempts!
```

---

## Controls & Feedback

- **Valid inputs** during guessing: an integer (1–100), `hint`, or `quit`.
- **Out-of-range** guesses are rejected without consuming an attempt.
- After each wrong guess you’ll see:
  - Direction: “greater than X” / “less than Y”
  - Proximity: “very hot (≤5)”, “warm (≤10)”, “cool (≤20)”, or “cold (>20)”
- **Hints** (manual):
  - **Range** narrowing (current min/max possible)
  - **Parity** (even/odd)
  - **Divisibility** (by 3, 5, or 7) or not divisible by any of them
  - **Proximity** bucket based on remaining range size
- **Auto-hint**: when only **2 or 1 attempts** remain and there are unused hint categories, you get a free hint.

> Manual hints **consume 1 attempt**. Auto-hints are **free**.

---

## High Scores

High scores are tracked per difficulty as the **fewest attempts** and stored in `high_scores.json` in the same directory.  
If no score is set yet for a difficulty, it shows as `None`.

**Example `high_scores.json`:**

```json
{
  "Easy": 7,
  "Medium": 5,
  "Hard": null
}
```

To reset all high scores, delete `high_scores.json` and run the game again.

---

## Internals (How It Works)

- The game keeps a current **possible range** (`min_possible`, `max_possible`) and updates it after each guess.
- `next_hint(...)` cycles through hint categories so you don’t get the same hint repeatedly.
- **Timer** starts at the beginning of each round and stops on success.
- On a win, the game **updates high scores** if you beat (or set) the record for the selected difficulty.

Key files/constants:
- **`HIGHSCORE_FILE`** → `high_scores.json`
- **Difficulties** → `{'Easy': 10, 'Medium': 5, 'Hard': 3}`

---

## Troubleshooting

- **“Please enter a valid number, 'hint', or 'quit'.”** → Your input wasn’t an integer/recognized command.
- **“Your guess must be between 1 and 100.”** → Guess was out of range.
- **Corrupt `high_scores.json`** → The game will safely ignore and recreate default values.
- On Windows, if `python` doesn’t work, try `py`:
  ```powershell
  py number_guess.py
  ```

---

## Extend the Game (Ideas)

- Persist last round stats (win/lose, time, last number)
- Leaderboard by player name
- Configurable range (e.g., 1–1000) and dynamic difficulty
- Colored CLI output for feedback and hints
- Unit tests for hint logic and scoring

---

## License

MIT — Have fun and hack away!
