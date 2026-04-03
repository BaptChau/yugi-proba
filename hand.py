"""Hand generator: draws a random opening hand from the main deck."""

import random
from deck import parse_deck, has_starter


def draw_hand(hand_size: int, pool: list[str]) -> list[str]:
    """Draw hand_size cards at random from the provided pool."""
    if hand_size > len(pool):
        raise ValueError(f"Hand size {hand_size} exceeds deck size {len(pool)}")
    return random.sample(pool, hand_size)


def run() -> None:
    try:
        hand_size = int(input("Hand size (default 5): ").strip() or "5")
    except ValueError:
        print("Invalid number.")
        return

    deck, starters = parse_deck("list.txt")
    pool: list[str] = [card for card, qty in deck.items() for _ in range(qty)]
    hand = draw_hand(hand_size, pool)

    print(f"\nOpening hand ({hand_size} cards):")
    for i, card in enumerate(hand, 1):
        tag = " [starter]" if card in starters else ""
        print(f"  {i}. {card}{tag}")

    print()
    if has_starter(hand, starters):
        starters_in_hand = [c for c in hand if c in starters]
        print(f"Starter(s): {', '.join(starters_in_hand)}")
    else:
        print("No starter in this hand.")
