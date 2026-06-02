"""
Turn-Based Battle Simulator
============================
A retro-RPG combat engine. Fight a Goblin using sword attacks, potions,
or run away. The monster counter-attacks every turn unless defeated.
"""

import random


def draw_health_bar(current_hp: int, max_hp: int = 50, symbol: str = "#") -> str:
    """Return a visual health bar: 1 symbol per 10 HP (rounded up)."""
    bars = max(0, -(-current_hp // 10))          # ceiling division
    return symbol * bars + f" ({current_hp})"


def main():
    # ------------------------------------------------------------------ #
    # Initialise state                                                      #
    # ------------------------------------------------------------------ #
    PLAYER_MAX_HP = 50
    player_hp:   int = PLAYER_MAX_HP
    monster_hp:  int = 50
    potions:     int = 3

    print("\n" + "=" * 40)
    print("        ⚔  BATTLE START  ⚔")
    print("=" * 40)
    print("A wild Goblin appears!\n")

    # ------------------------------------------------------------------ #
    # Main game loop – runs while both combatants are alive                #
    # ------------------------------------------------------------------ #
    while player_hp > 0 and monster_hp > 0:

        # Display HUD
        print(f"\nPlayer Health : {draw_health_bar(player_hp)}")
        print(f"Monster Health: {monster_hp}")
        print(f"Potions left  : {potions}")
        print("-" * 30)
        print("1. Sword Attack")
        print("2. Drink Potion")
        print("3. Run Away")

        # ---- get player action ---------------------------------------- #
        try:
            action = int(input("\nChoose action: ").strip())
        except ValueError:
            print("\n⚠  Invalid Input! Please enter 1, 2, or 3.")
            continue                          # monster does NOT attack on bad input

        if action not in (1, 2, 3):
            print("\n⚠  Invalid Input! Please enter 1, 2, or 3.")
            continue

        monster_attacks = True               # flag: monster counter-attacks by default

        # ---- option 1: sword attack ----------------------------------- #
        if action == 1:
            damage = 10
            monster_hp -= damage
            print(f"\n> You hit the Goblin for {damage} damage!")
            if monster_hp <= 0:
                monster_hp = 0
                monster_attacks = False      # monster is dead – no counter-attack

        # ---- option 2: drink potion ----------------------------------- #
        elif action == 2:
            if potions > 0:
                heal = 15
                player_hp = min(PLAYER_MAX_HP, player_hp + heal)  # cap at max HP
                potions -= 1
                print(f"\n> You drank a potion. Recovered {heal} HP.")
                print(f"> Potions remaining: {potions}")
            else:
                print("\n> No potions left!")

        # ---- option 3: run away --------------------------------------- #
        elif action == 3:
            print("\n> You ran away! (Coward… but alive.)")
            print("=" * 40)
            return                           # exit the game entirely

        # ---- monster counter-attack ----------------------------------- #
        if monster_attacks and monster_hp > 0:
            monster_damage = random.randint(5, 15)
            player_hp -= monster_damage
            player_hp = max(0, player_hp)
            print(f"> The Goblin attacks you for {monster_damage} damage!")

    # ------------------------------------------------------------------ #
    # Post-loop: determine outcome                                          #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 40)
    if monster_hp <= 0 and player_hp > 0:
        print("🏆  You defeated the Goblin!  VICTORY!")
    elif player_hp <= 0 and monster_hp > 0:
        print("💀  You were defeated...  GAME OVER.")
    else:
        # Edge case: both reach 0 on the same turn
        print("💥  Mutual destruction! It's a draw.")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    main()
