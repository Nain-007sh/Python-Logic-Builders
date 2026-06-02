"""
Recursive File Explorer
========================
Navigates a nested-dictionary file system, recursively calculates folder
sizes, and provides an interactive CLI menu.
"""

from typing import Union

# ------------------------------------------------------------------ #
# The "Hard Drive" data structure (exact structure from the PDF)       #
# ------------------------------------------------------------------ #
file_system: dict = {
    "root": {
        "documents": {
            "resume.txt": 15,
            "budget.xls": 30,
            "old_stuff": {
                "letters": {
                    "love_letter.txt": 2,
                    "breakup_letter.txt": 2
                },
                "school": {
                    "homework.docx": 10
                }
            }
        },
        "photos": {
            "cat.jpg": 100,
            "dog.png": 105,
            "vacation": {
                "beach.png": 200,
                "mountain.jpg": 200
            }
        },
        "system_log.txt": 50
    }
}


# ------------------------------------------------------------------ #
# Part A – Recursive size calculator                                   #
# ------------------------------------------------------------------ #
def calculate_size(current_item: Union[int, dict], indent: int = 0) -> int:
    """
    Recursively calculate the total size of a file-system item.

    Base case  : current_item is an int  → it's a file; return its size.
    Recursive  : current_item is a dict  → it's a folder; sum children.
    """
    prefix = "  " * indent          # visual indentation for output

    # Base case – it's a file (integer size)
    if isinstance(current_item, int):
        return current_item

    # Recursive case – it's a folder (dictionary)
    if isinstance(current_item, dict):
        total = 0
        for name, content in current_item.items():
            if isinstance(content, int):
                # File found
                print(f"{prefix}> Found file: {name} ({content} MB)")
                total += calculate_size(content, indent)
            elif isinstance(content, dict):
                # Sub-folder found – recurse
                print(f"{prefix}> Entering subfolder '{name}'...")
                total += calculate_size(content, indent + 1)
            else:
                # Unexpected type – skip gracefully
                print(f"{prefix}⚠  Unexpected item '{name}' – skipping.")
        return total

    # Fallback for any unexpected type
    print(f"⚠  Unrecognised item type: {type(current_item)} – skipping.")
    return 0


# ------------------------------------------------------------------ #
# Helper – deep search for a folder name anywhere in the tree          #
# ------------------------------------------------------------------ #
def find_folder(tree: dict, target: str) -> Union[dict, None]:
    """
    Recursively search the entire tree for a folder named `target`.
    Returns the folder dict if found, otherwise None.
    """
    for name, content in tree.items():
        if name == target and isinstance(content, dict):
            return content
        if isinstance(content, dict):
            result = find_folder(content, target)
            if result is not None:
                return result
    return None


# ------------------------------------------------------------------ #
# Part B – Interactive menu                                            #
# ------------------------------------------------------------------ #
def main_menu() -> None:
    # Start inside "root" for a cleaner experience
    root: dict = file_system.get("root", file_system)
    top_level_names = list(root.keys())

    print("\n" + "=" * 45)
    print("        --- FILE SYSTEM SCANNER ---")
    print("=" * 45)

    while True:
        print(f"\nCurrent Root Folders: {top_level_names}")
        folder_input = input("\nEnter a folder name to scan (or 'exit'): ").strip()

        if folder_input.lower() == "exit":
            print("\nGoodbye! 👋\n")
            break

        # ---- Part C – exception handling ----------------------------- #
        try:
            # First try top-level keys inside root
            if folder_input in root:
                folder_content = root[folder_input]
                if isinstance(folder_content, int):
                    # It's a file, not a folder
                    print(f"\n'{folder_input}' is a file ({folder_content} MB), not a folder.")
                    continue
            else:
                # Deep search across the whole tree
                folder_content = find_folder(root, folder_input)
                if folder_content is None:
                    raise KeyError(folder_input)

            print(f"\n> Scanning '{folder_input}'...")
            print("-" * 35)
            total = calculate_size(folder_content, indent=0)
            print("-" * 35)
            print(f"TOTAL SIZE: {total} MB\n")

        except KeyError:
            print(f"\n⚠  Error: Folder '{folder_input}' does not exist in the file system!")
        except Exception as e:
            print(f"\n⚠  Unexpected error while scanning '{folder_input}': {e}")


if __name__ == "__main__":
    main_menu()
