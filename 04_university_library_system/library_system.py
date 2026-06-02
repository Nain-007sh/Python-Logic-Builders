"""
University Library & Staff System
===================================
OOP solution with:
  - Class hierarchy  : Person → Member / Employee → StudentWorker
  - Multiple inheritance for StudentWorker
  - File I/O         : reads library_people.txt, writes payroll_report.txt
  - Recursion        : get_total_hierarchy_cost() walks the employee tree
"""

from __future__ import annotations
import os


# ================================================================== #
# Level 1 – Base Class                                                #
# ================================================================== #
class Person:
    """Represents any person in the library system."""

    def __init__(self, id_number: int, name: str) -> None:
        self.id_number: int = id_number
        self.name:      str = name.strip()

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] ID={self.id_number}  Name={self.name}"


# ================================================================== #
# Level 2 – Parent Classes                                            #
# ================================================================== #
class Member(Person):
    """A student member who owes membership fees."""

    def __init__(self, id_number: int, name: str, membership_fees_owed: float) -> None:
        Person.__init__(self, id_number, name)   # explicit call avoids MRO collision
        self.membership_fees_owed: float = membership_fees_owed

    def pay_fees(self, amount: float) -> None:
        """Reduce outstanding fees by the given amount (floor at 0)."""
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        self.membership_fees_owed = max(0.0, self.membership_fees_owed - amount)
        print(f"  {self.name} paid ${amount:,.2f}. Remaining fees: ${self.membership_fees_owed:,.2f}")

    def __str__(self) -> str:
        return super().__str__() + f"  Fees Owed=${self.membership_fees_owed:,.2f}"


class Employee(Person):
    """A library employee with a salary and optional subordinates."""

    def __init__(self, id_number: int, name: str, salary: float) -> None:
        Person.__init__(self, id_number, name)   # explicit call avoids MRO collision
        self.salary:       float         = salary
        self.subordinates: list[Employee] = []

    def add_subordinate(self, employee: Employee) -> None:
        """Add a direct report to this employee."""
        self.subordinates.append(employee)

    def get_total_hierarchy_cost(self) -> float:
        """
        Recursively sum salaries for this employee and all subordinates.

        Base case  : no subordinates → return own salary.
        Recursive  : salary + sum of each subordinate's hierarchy cost.
        """
        total = self.salary
        for sub in self.subordinates:
            total += sub.get_total_hierarchy_cost()
        return total

    def hierarchy_report(self, depth: int = 0) -> str:
        """Return a formatted string showing the reporting tree."""
        indent = "    " * depth
        lines  = [f"{indent}↳ {self.name}  (${self.salary:,.2f}/yr)"]
        for sub in self.subordinates:
            lines.append(sub.hierarchy_report(depth + 1))
        return "\n".join(lines)

    def __str__(self) -> str:
        return super().__str__() + f"  Salary=${self.salary:,.2f}"


# ================================================================== #
# Level 3 – Child Class (Multiple Inheritance)                        #
# ================================================================== #
class StudentWorker(Member, Employee):
    """
    A student who also works part-time at the library.
    Inherits Member (pays fees) and Employee (earns salary).
    MRO: StudentWorker → Member → Employee → Person
    """

    def __init__(
        self,
        id_number: int,
        name: str,
        salary: float,
        membership_fees_owed: float
    ) -> None:
        # Explicitly initialise both parents to avoid MRO ambiguity
        Employee.__init__(self, id_number, name, salary)
        Member.__init__(self, id_number, name, membership_fees_owed)

    def net_income(self) -> float:
        """Return take-home pay after membership fees."""
        return self.salary - self.membership_fees_owed

    def __str__(self) -> str:
        return (
            f"[StudentWorker] ID={self.id_number}  Name={self.name}"
            f"  Salary=${self.salary:,.2f}"
            f"  Fees Owed=${self.membership_fees_owed:,.2f}"
            f"  Net Income=${self.net_income():,.2f}"
        )


# ================================================================== #
# Part A – File Reading & Object Creation                             #
# ================================================================== #
def load_people(filepath: str) -> dict[int, Person]:
    """
    Read library_people.txt and return a dict keyed by ID.
    Skips malformed lines with a printed warning.

    File format:
      E, id, name, salary, reports_to_id
      M, id, name, fees_owed, 0
      S, id, name, salary, fees_owed, reports_to_id
    """
    people: dict[int, Person] = {}

    if not os.path.exists(filepath):
        print(f"❌  File not found: {filepath}")
        return people

    with open(filepath, "r", encoding="utf-8") as fh:
        for line_num, raw_line in enumerate(fh, start=1):
            line = raw_line.strip()
            if not line:
                continue                          # skip blank lines

            parts = [p.strip() for p in line.split(",")]
            record_type = parts[0].upper()

            try:
                # ---- Employee ---------------------------------------- #
                if record_type == "E":
                    _, id_str, name, salary_str, _ = parts
                    person = Employee(
                        id_number = int(id_str),
                        name      = name,
                        salary    = float(salary_str)
                    )

                # ---- Member ------------------------------------------ #
                elif record_type == "M":
                    _, id_str, name, fees_str, _ = parts
                    person = Member(
                        id_number            = int(id_str),
                        name                 = name,
                        membership_fees_owed = float(fees_str)
                    )

                # ---- StudentWorker ------------------------------------ #
                elif record_type == "S":
                    _, id_str, name, salary_str, fees_str, _ = parts
                    person = StudentWorker(
                        id_number            = int(id_str),
                        name                 = name,
                        salary               = float(salary_str),
                        membership_fees_owed = float(fees_str)
                    )

                else:
                    print(f"⚠  Line {line_num}: Unknown record type '{record_type}' – skipping.")
                    continue

            except (ValueError, IndexError) as exc:
                print(f"⚠  Error processing line {line_num} ('{line}'): {exc} – skipping.")
                continue

            people[person.id_number] = person
            print(f"  Loaded: {person}")

    return people


# ================================================================== #
# Part B – Linking Employees                                          #
# ================================================================== #
def link_subordinates(people: dict[int, Person], filepath: str) -> None:
    """
    Re-read the file purely for the reports_to_id column and wire up
    the Employee.subordinates lists.
    """
    with open(filepath, "r", encoding="utf-8") as fh:
        for line_num, raw_line in enumerate(fh, start=1):
            line  = raw_line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            rtype = parts[0].upper()

            try:
                if rtype == "E":
                    _, id_str, _name, _salary, reports_to_str = parts
                elif rtype == "S":
                    _, id_str, _name, _salary, _fees, reports_to_str = parts
                else:
                    continue                      # Members have no boss field

                emp_id      = int(id_str)
                reports_to  = int(reports_to_str)

                if reports_to == 0:
                    continue                      # top of the hierarchy

                subordinate = people.get(emp_id)
                manager     = people.get(reports_to)

                if subordinate and manager and isinstance(manager, Employee):
                    manager.add_subordinate(subordinate)   # type: ignore[arg-type]
                    print(f"  Linked: '{subordinate.name}' → reports to '{manager.name}'")

            except (ValueError, IndexError) as exc:
                print(f"⚠  Link error on line {line_num}: {exc} – skipping.")


# ================================================================== #
# Part D – Write Payroll Report                                       #
# ================================================================== #
def write_payroll_report(
    people:     dict[int, Person],
    output_path: str
) -> None:
    """Write a structured payroll report to payroll_report.txt."""

    # Find the root employee (reports_to == 0)
    root_employee: Employee | None = None
    for person in people.values():
        if isinstance(person, Employee) and not any(
            person in getattr(mgr, "subordinates", [])
            for mgr in people.values()
            if isinstance(mgr, Employee)
        ):
            root_employee = person
            break

    lines: list[str] = []
    lines.append("=" * 55)
    lines.append("       UNIVERSITY LIBRARY – PAYROLL REPORT")
    lines.append("=" * 55)
    lines.append("")

    # --- All people --------------------------------------------------- #
    lines.append("--- ALL REGISTERED PEOPLE ---")
    for person in people.values():
        lines.append(f"  {person}")
    lines.append("")

    # --- StudentWorker net incomes ------------------------------------ #
    lines.append("--- STUDENT WORKER NET INCOMES ---")
    for person in people.values():
        if isinstance(person, StudentWorker):
            lines.append(
                f"  {person.name:<20} Salary=${person.salary:>10,.2f}"
                f"  Fees=${person.membership_fees_owed:>8,.2f}"
                f"  Net=${person.net_income():>10,.2f}"
            )
    lines.append("")

    # --- Reporting hierarchy & total cost ---------------------------- #
    if root_employee:
        lines.append("--- REPORTING HIERARCHY ---")
        lines.append(root_employee.hierarchy_report())
        lines.append("")
        total_cost = root_employee.get_total_hierarchy_cost()
        lines.append("--- TOTAL SALARY BUDGET ---")
        lines.append(f"  Root    : {root_employee.name}")
        lines.append(f"  Budget  : ${total_cost:,.2f}")
    else:
        lines.append("⚠  Could not determine root employee for hierarchy cost.")

    lines.append("")
    lines.append("=" * 55)
    report_text = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(report_text)

    print(f"\n📄  Payroll report written to: {output_path}")
    print("\n" + report_text)


# ================================================================== #
# Main entry point                                                     #
# ================================================================== #
def main() -> None:
    data_file   = os.path.join(os.path.dirname(__file__), "library_people.txt")
    report_file = os.path.join(os.path.dirname(__file__), "payroll_report.txt")

    print("\n" + "=" * 45)
    print("   UNIVERSITY LIBRARY SYSTEM – LOADING")
    print("=" * 45 + "\n")

    # Part A – load objects
    print("--- Loading People ---")
    people = load_people(data_file)

    if not people:
        print("No people loaded. Exiting.")
        return

    # Part B – link subordinates
    print("\n--- Linking Reporting Structure ---")
    link_subordinates(people, data_file)

    # Parts C + D – compute costs and write report
    print()
    write_payroll_report(people, report_file)


if __name__ == "__main__":
    main()
