"""
CLI Bank ATM
============
A command-line ATM simulator with deposit, withdrawal, balance check,
and transaction history (extra credit).
"""

import random


def main():
    # ------------------------------------------------------------------ #
    # Initialise state                                                      #
    # ------------------------------------------------------------------ #
    balance: float = round(random.uniform(500, 5000), 2)   # bonus: randomised
    history: list[str] = []                                  # extra-credit log

    print("\n" + "=" * 40)
    print("     WELCOME TO UPSKILL BANK")
    print("=" * 40)

    # ------------------------------------------------------------------ #
    # Main loop – keeps running until the user selects Exit                #
    # ------------------------------------------------------------------ #
    while True:
        print(f"\n--- UPSKILL BANK ATM ---")
        print(f"Current Balance: ${balance:,.2f}")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Print Statement")
        print("4. Exit")

        # ---- menu choice ---------------------------------------------- #
        try:
            choice = int(input("\nSelect an option: ").strip())
        except ValueError:
            print("\n⚠  Invalid input, please enter a number.")
            continue

        # ---- option 1: deposit ---------------------------------------- #
        if choice == 1:
            try:
                amount = float(input("Enter amount to deposit: $").strip())
            except ValueError:
                print("\n⚠  Error: Please enter a valid number!")
                continue

            if amount <= 0:
                print("\n⚠  Deposit amount must be greater than zero.")
                continue

            balance += amount
            entry = f"Deposited  ${amount:>10,.2f}  |  Balance: ${balance:,.2f}"
            history.append(entry)
            print(f"\n✅ ${amount:,.2f} deposited. New Balance: ${balance:,.2f}")

        # ---- option 2: withdraw --------------------------------------- #
        elif choice == 2:
            try:
                amount = float(input("Enter amount to withdraw: $").strip())
            except ValueError:
                print("\n⚠  Error: Please enter a valid number!")
                continue

            if amount <= 0:
                print("\n⚠  Withdrawal amount must be greater than zero.")
                continue

            if amount > balance:
                print(f"\n⚠  Error: Insufficient funds! You only have ${balance:,.2f}.")
                continue

            balance -= amount
            entry = f"Withdrew   ${amount:>10,.2f}  |  Balance: ${balance:,.2f}"
            history.append(entry)
            print(f"\n✅ ${amount:,.2f} withdrawn. New Balance: ${balance:,.2f}")

        # ---- option 3: print statement (extra credit) ----------------- #
        elif choice == 3:
            print("\n--- TRANSACTION STATEMENT ---")
            if not history:
                print("  No transactions yet.")
            else:
                for i, record in enumerate(history, start=1):
                    print(f"  {i:>3}. {record}")
            print(f"\n  Current Balance: ${balance:,.2f}")
            print("-----------------------------")

        # ---- option 4: exit ------------------------------------------- #
        elif choice == 4:
            print("\n👋 Thank you for banking with us. Goodbye!\n")
            break

        else:
            print("\n⚠  Invalid option. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
