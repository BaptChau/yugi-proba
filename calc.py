"""Probability calculator: P(opening all target cards in hand)."""

from math import comb
from itertools import combinations
from deck import parse_deck, find_card, has_starter


def prob_open_all(deck: dict[str, int], hand_size: int, targets: list[str]) -> float:
    """
    P(at least 1 copy of each target card in opening hand).

    Uses inclusion-exclusion over the hypergeometric distribution:
      P = Σ (-1)^|S| * C(total - Σ copies(S), hand_size) / C(total, hand_size)
    """
    total = sum(deck.values())
    quantities = [deck[card] for card in targets]
    k = len(quantities)
    denom = comb(total, hand_size)

    result = 0
    for size in range(k + 1):
        sign = (-1) ** size
        for subset in combinations(range(k), size):
            excluded = sum(quantities[i] for i in subset)
            remaining = total - excluded
            ways = comb(remaining, hand_size) if remaining >= hand_size else 0
            result += sign * ways

    return result / denom


def run() -> None:
    deck, starters = parse_deck("list.txt")
    total = sum(deck.values())

    try:
        hand_size = int(input("Hand size (default 5): ").strip() or "5")
    except ValueError:
        print("Invalid number.")
        return

    if hand_size < 1 or hand_size > total:
        print(f"Hand size must be between 1 and {total}.")
        return

    print("Enter card names one per line, empty line to finish:")
    card_names: list[str] = []
    while True:
        name = input("  Card: ").strip()
        if not name:
            break
        found = find_card(name, deck)
        if found is None:
            print(f"  '{name}' not found in main deck, skipping.")
        else:
            card_names.append(found)
            tag = " [starter]" if found in starters else ""
            print(f"  -> {deck[found]}x {found}{tag}")

    if not card_names:
        print("No cards selected.")
        return

    if hand_size < len(card_names):
        print("Probability: 0.00% (more targets than hand size)")
        return

    print(f"\nDeck size : {total}")
    print(f"Hand size : {hand_size}")
    print("Targets   :", ", ".join(f"{deck[c]}x {c}" for c in card_names))

    has_any_starter = any(c in starters for c in card_names)
    if has_any_starter:
        starter_targets = [c for c in card_names if c in starters]
        print(f"Starters  : {', '.join(starter_targets)}")

    prob = prob_open_all(deck, hand_size, card_names)
    print(f"\nProbability: {prob:.4%}  ({prob:.6f})")
