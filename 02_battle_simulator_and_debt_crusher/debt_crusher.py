"""
The Debt Crusher – Amortization Calculator
==========================================
Simulates a loan repayment schedule month by month.
Handles the "Logic Trap" (payment < interest) and "Final Month Twist".
"""


def get_positive_float(prompt: str) -> float:
    """
    Keep asking until the user gives a valid positive number.
    Strips common non-numeric characters like '$', '%', ',' before parsing.
    """
    while True:
        raw = input(prompt).strip()
        cleaned = raw.replace("$", "").replace("%", "").replace(",", "")
        try:
            value = float(cleaned)
            if value <= 0:
                print("⚠  Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("⚠  Invalid input. Please enter a plain number (e.g. 5000, not $5,000).")


def main():
    print("\n" + "=" * 40)
    print("       --- LOAN CALCULATOR ---")
    print("=" * 40 + "\n")

    # ------------------------------------------------------------------ #
    # Gather inputs                                                         #
    # ------------------------------------------------------------------ #
    principal       = get_positive_float("Enter Loan Amount          : $")
    annual_rate_pct = get_positive_float("Enter Annual Interest Rate  : % ")
    monthly_payment = get_positive_float("Enter Monthly Payment       : $")

    # Convert annual rate to a monthly decimal rate
    monthly_rate = (annual_rate_pct / 100) / 12

    # ------------------------------------------------------------------ #
    # Logic Trap: if first month's interest >= monthly payment, loan       #
    # will never be paid off.                                              #
    # ------------------------------------------------------------------ #
    first_interest = principal * monthly_rate
    if monthly_payment <= first_interest:
        print(
            f"\n❌  You will never pay this off!\n"
            f"    First month's interest alone is ${first_interest:,.2f}, "
            f"but your payment is only ${monthly_payment:,.2f}.\n"
            f"    Increase your monthly payment above ${first_interest:,.2f} to make progress."
        )
        return

    # ------------------------------------------------------------------ #
    # Amortisation loop                                                    #
    # ------------------------------------------------------------------ #
    print("\nCalculating...\n")
    print("-" * 50)

    balance           = principal
    month             = 0
    total_interest    = 0.0

    while balance > 0:
        month += 1

        # Monthly interest on current balance
        interest = balance * monthly_rate

        # Final Month Twist: only pay the remaining balance (+ last interest)
        actual_payment = min(monthly_payment, balance + interest)
        principal_paid = actual_payment - interest
        balance        = max(0.0, balance - principal_paid)

        total_interest += interest

        # Annotate the final payment
        final_flag = " (Final Payment)" if balance == 0.0 else ""

        print(f"Month {month}:")
        print(f"  Interest       : ${interest:>10,.2f}")
        print(f"  Principal Paid : ${principal_paid:>10,.2f}{final_flag}")
        print(f"  Remaining Bal  : ${balance:>10,.2f}")
        print()

    # ------------------------------------------------------------------ #
    # Summary                                                              #
    # ------------------------------------------------------------------ #
    print("-" * 50)
    print(f"✅  TOTAL: Paid off in {month} month{'s' if month != 1 else ''}.")
    print(f"    Total Interest Paid: ${total_interest:,.2f}\n")


if __name__ == "__main__":
    main()
