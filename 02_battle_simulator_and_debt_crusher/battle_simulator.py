import random

player_hp = 50
monster_hp = 50
potions = 3

print("--- BATTLE START ---")

while player_hp > 0 and monster_hp > 0:
    # Health Bar (1 # for every 10 HP)
    health_bar = "#" * (player_hp // 10)

    print(f"\nPlayer Health: {health_bar} ({player_hp})")
    print(f"Monster Health: {monster_hp}")
    print(f"Potions left: {potions}")

    print("1. Sword Attack")
    print("2. Drink Potion")
    print("3. Run Away")


    try:
        choice = int(input("Choose action: "))
    except:
        print(" Invalid Input! Please enter 1, 2, or 3.")
        continue


    if choice == 1:
        print("> You hit the monster for 10 damage!")
        monster_hp -= 10

    elif choice == 2:
        if potions > 0:
            player_hp += 15
            potions -= 1
            print("> You drank a potion and recovered 15 HP.")
        else:
            print("> No potions left!")
            continue

    elif choice == 3:
        print("> You ran away safely!")
        break

    else:
        print("> Invalid choice!")
        continue

    if monster_hp > 0:
        damage = random.randint(5, 15)
        print(f"> The monster attacks you for {damage} damage!")
        player_hp -= damage

if player_hp <= 0:
    print("\nYou were defeated... 💀")
elif monster_hp <= 0:
    print("\nYou defeated the Goblin! 🎉")

