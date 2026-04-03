#!/usr/bin/env python3
"""Yu-Gi-Oh tools launcher."""

import importlib

PROGRAMS = {
    "1": ("Probability calculator",        "calc"),
    "2": ("Hand generator",                "hand"),
    "3": ("Mass hand generator",           "mass_hand"),
    "4": ("Starter probability",           "starter_prob"),
}


def show_menu() -> None:
    print("\n=== Yu-Gi-Oh Tools ===")
    for key, (label, _) in PROGRAMS.items():
        print(f"  {key}. {label}")
    print("  q. Quit")


def main() -> None:
    while True:
        show_menu()
        choice = input("\nChoose: ").strip().lower()

        if choice == "q":
            break

        if choice not in PROGRAMS:
            print("Invalid choice.")
            continue

        label, module_name = PROGRAMS[choice]
        print(f"\n--- {label} ---")
        try:
            module = importlib.import_module(module_name)
            module.run()
        except KeyboardInterrupt:
            print("\nCancelled.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
