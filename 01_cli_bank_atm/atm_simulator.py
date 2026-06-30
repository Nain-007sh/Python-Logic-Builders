account_balance = 10000

def show_balance():
    print(f"Available Balance: ${account_balance}")

def add_money():
    # while True:
        try:
            global account_balance
            amount = int(input("Enter amount to add: "))
            account_balance += amount
            print(f"${amount} added successfully!")
            show_balance()
        except:
            print("enter sufficient value ")

def take_money():
    try:
       global account_balance
       amount = int(input("Enter amount to withdraw: "))
       if amount > account_balance:

        print("Transaction failed! Not enough funds.")
       else:
        account_balance -= amount
        print(f"${amount} withdrawn successfully!")
        show_balance()
    except:
        print("enter sufficient value")


while True:
    try:
        print("=== UPSKILL DIGITAL ATM ===")
        print(f"Balance: ${account_balance}")
        print("1 → Deposit Money")
        print("2 → Withdraw Money")
        print("3 → Check Balance")
        print("4 → Quit")

        choice = int(input("Select your option: "))

        if choice == 1:
            add_money()
        elif choice == 2:
            take_money()
        elif choice == 3:
            show_balance()
        elif choice == 4:
            print("Thank you for using Upskill Digital ATM!")
            break
        else:
            print("Invalid input! Please select a number between 1–4.")

    except:
        print("Invalid value entered please try again ")
