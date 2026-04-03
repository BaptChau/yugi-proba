# yugi-proba

A command-line toolkit to analyse the probability of your Yu-Gi-Oh! opening hands.

## Requirements

Python 3.10+ — no external dependencies.

## Getting started

### 1. Set up your deck list

Edit `list.txt` to match your deck. The file is divided into sections:

```
Monstre
3 Card Name
1 Another Card -- starter
Magie
3 Spell Card -- starter
Piège
2 Trap Card
Extra
1 Extra Deck Monster
côté
3 Side Deck Card
```

Rules:
- Only `Monstre`, `Magie`, and `Piège` are counted as the main deck.
- Add `-- starter` at the end of a line to tag a card as a starter (a card that can start your combo).

### 2. Launch the app

```bash
python main.py
```

You will see the main menu:

```
=== Yu-Gi-Oh Tools ===
  1. Probability calculator
  2. Hand generator
  3. Mass hand generator
  4. Starter probability
  q. Quit
```

---

## Tools

### 1. Probability calculator

Calculates the exact probability of opening **all** specified cards together in your starting hand.

Internally uses the **multivariate hypergeometric distribution** with inclusion-exclusion:

```
P = Σ (-1)^|S| × C(total − Σ copies(S), hand_size) / C(total, hand_size)
```

**Usage:**
1. Enter your hand size (default: 5).
2. Enter card names one by one (partial/case-insensitive names are accepted). Empty line to confirm.
3. The probability is displayed as a percentage.

Cards tagged as starters are highlighted with `[starter]` during input.

---

### 2. Hand generator

Draws a random opening hand from your main deck.

- Enter your hand size (default: 5).
- Each card in the hand is displayed, with `[starter]` tags where applicable.
- A summary line tells you whether the hand contains at least one starter.

---

### 3. Mass hand generator

Simulates a large number of opening hands and exports the results to `hands.json`.

- Enter your hand size (default: 5) and number of simulations (default: 300).
- Results are saved to `hands.json` with each hand, a `has_starter` flag per hand, and a `"starter": true/false` flag per card.
- Terminal output shows:
  - Number of unique hand combinations
  - **Hands without a starter** — count and percentage
  - **Most frequent** hand
  - **Least frequent** hand

> With a 40-card deck, nearly every hand will be unique over 300 draws due to combinatorial explosion. Increase the run count (e.g. 10 000) for more meaningful frequency stats.

---

### 4. Starter probability

Calculates the probability of opening **at least one starter** in your hand using the hypergeometric distribution:

```
P(at least 1 starter) = 1 − C(non-starters, hand_size) / C(total, hand_size)
```

- Lists every card tagged `-- starter` in your deck with its copy count.
- Displays the probability for the chosen hand size.

---

## Project structure

```
main.py         — interactive launcher menu
deck.py         — shared deck parser (parse_deck, find_card, has_starter)
calc.py         — probability calculator logic
hand.py         — single hand generator
mass_hand.py    — mass simulation and JSON export
starter_prob.py — starter probability calculator
list.txt        — your deck list
```

---

## Contributing

Contributions are welcome! If you have an idea for a new tool or an improvement to an existing one:

1. **Fork** this repository.
2. Create a new branch: `git checkout -b feature/my-tool`.
3. Make your changes. If adding a new program, create a module with a `run()` function and register it in the `PROGRAMS` dict in `main.py`.
4. Open a **Pull Request** with a description of what you added and why.

All skill levels are welcome.
