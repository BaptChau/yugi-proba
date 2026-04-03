"""Mass hand generator: simulate N hands, export to JSON, show frequency stats."""

import json
from collections import Counter
from deck import parse_deck, has_starter
from hand import draw_hand

OUTPUT_FILE = "hands.json"
DEFAULT_RUNS = 300
STATS_ONLY_THRESHOLD = 10_000


def simulate(hand_size: int, runs: int, pool: list[str]) -> list[list[str]]:
    """Draw `runs` hands of `hand_size` cards each."""
    return [draw_hand(hand_size, pool) for _ in range(runs)]


def hand_key(hand: list[str]) -> tuple[str, ...]:
    """Canonical form of a hand: sorted tuple (order-independent)."""
    return tuple(sorted(hand))


def run() -> None:
    try:
        hand_size = int(input("Hand size (default 5): ").strip() or "5")
    except ValueError:
        print("Invalid number.")
        return

    try:
        runs = int(input(f"Number of hands (default {DEFAULT_RUNS}): ").strip() or str(DEFAULT_RUNS))
    except ValueError:
        print("Invalid number.")
        return

    deck, starters = parse_deck("list.txt")
    total = sum(deck.values())
    if hand_size < 1 or hand_size > total:
        print(f"Hand size must be between 1 and {total}.")
        return

    pool: list[str] = [card for card, qty in deck.items() for _ in range(qty)]

    print(f"\nSimulating {runs} hands of {hand_size} cards...")
    hands = simulate(hand_size, runs, pool)

    # --- starter analysis ---
    no_starter_hands = [h for h in hands if not has_starter(h, starters)]
    no_starter_count = len(no_starter_hands)

    # --- frequency analysis ---
    counter: Counter[tuple[str, ...]] = Counter(hand_key(h) for h in hands)
    most_common = counter.most_common()
    best_hand, best_count = most_common[0]
    worst_hand, worst_count = most_common[-1]

    def hand_json(hand: list[str]) -> list[dict]:
        return [{"card": c, "starter": c in starters} for c in hand]

    stats_only = runs > STATS_ONLY_THRESHOLD

    # --- JSON output ---
    output: dict = {
        "settings": {"hand_size": hand_size, "runs": runs, "stats_only": stats_only},
        "stats": {
            "unique_hands": len(counter),
            "no_starter": {
                "count": no_starter_count,
                "percentage": round(no_starter_count / runs * 100, 2),
            },
            "most_frequent": {
                "cards": list(best_hand),
                "starters": [c for c in best_hand if c in starters],
                "count": best_count,
                "percentage": round(best_count / runs * 100, 2),
            },
            "least_frequent": {
                "cards": list(worst_hand),
                "starters": [c for c in worst_hand if c in starters],
                "count": worst_count,
                "percentage": round(worst_count / runs * 100, 2),
            },
        },
    }

    if not stats_only:
        output["hands"] = [
            {
                "id": i + 1,
                "cards": hand_json(h),
                "has_starter": has_starter(h, starters),
            }
            for i, h in enumerate(hands)
        ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    if stats_only:
        print(f"Saved stats to {OUTPUT_FILE} (hands omitted, run count > {STATS_ONLY_THRESHOLD:,})\n")
    else:
        print(f"Saved {runs} hands to {OUTPUT_FILE}\n")

    print(f"Unique hand combinations : {len(counter)}")
    print(f"Hands without a starter  : {no_starter_count}/{runs} ({no_starter_count/runs:.1%})")
    print()
    print(f"Most frequent ({best_count}/{runs} = {best_count/runs:.1%}):")
    for card in best_hand:
        tag = " [starter]" if card in starters else ""
        print(f"  - {card}{tag}")
    print()
    print(f"Least frequent ({worst_count}/{runs} = {worst_count/runs:.1%}):")
    for card in worst_hand:
        tag = " [starter]" if card in starters else ""
        print(f"  - {card}{tag}")
