"""Shared deck parser."""

MAIN_SECTIONS = {"Monstre", "Magie", "Piège"}
ALL_SECTIONS = {"Monstre", "Magie", "Piège", "Extra", "côté"}
STARTER_TAG = "-- starter"


def parse_deck(filepath: str = "list.txt") -> tuple[dict[str, int], set[str]]:
    """
    Return (deck, starters) for the main deck (Monstre, Magie, Piège only).
    deck    : {card_name: quantity}
    starters: set of card names tagged '-- starter'
    """
    deck: dict[str, int] = {}
    starters: set[str] = set()
    current_section = None

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line in ALL_SECTIONS:
                current_section = line
                continue
            if current_section in MAIN_SECTIONS:
                is_starter = STARTER_TAG in line
                clean = line.replace(STARTER_TAG, "").strip()
                parts = clean.split(" ", 1)
                if len(parts) == 2:
                    try:
                        name = parts[1]
                        deck[name] = int(parts[0])
                        if is_starter:
                            starters.add(name)
                    except ValueError:
                        pass
    return deck, starters


def find_card(name: str, deck: dict[str, int]) -> str | None:
    """Resolve a card name: exact → case-insensitive → unambiguous substring."""
    if name in deck:
        return name
    lower = name.lower()
    for card in deck:
        if card.lower() == lower:
            return card
    matches = [card for card in deck if lower in card.lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"Ambiguous name '{name}', matches: {matches}")
    return None


def has_starter(hand: list[str], starters: set[str]) -> bool:
    return any(card in starters for card in hand)
