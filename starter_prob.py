"""Probability of opening at least one starter in hand."""

from math import comb
from deck import parse_deck


def prob_at_least_one_starter(total: int, starter_copies: int, hand_size: int) -> float:
    """P(at least 1 starter) = 1 - P(0 starters) via hypergeometric."""
    non_starters = total - starter_copies
    p_none = comb(non_starters, hand_size) / comb(total, hand_size)
    return 1 - p_none


def run() -> None:
    deck, starters = parse_deck("list.txt")
    total = sum(deck.values())
    starter_copies = sum(deck[c] for c in starters)

    try:
        hand_size = int(input("Hand size (default 5): ").strip() or "5")
    except ValueError:
        print("Invalid number.")
        return

    if hand_size < 1 or hand_size > total:
        print(f"Hand size must be between 1 and {total}.")
        return

    print(f"\nDeck size     : {total}")
    print(f"Starter cards : {starter_copies} copies across {len(starters)} unique cards")
    print(f"  " + "\n  ".join(f"{deck[c]}x {c}" for c in sorted(starters)))
    print(f"Hand size     : {hand_size}")

    prob = prob_at_least_one_starter(total, starter_copies, hand_size)
    print(f"\nP(at least 1 starter): {prob:.4%}  ({prob:.6f})")
