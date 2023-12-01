import sys


def delete_last_line():
    """Deletes the last line in the STDOUT"""
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


def require_input_and_clear(prompt):
    """Print the prompt, get user input, clear the prompt, and return the input."""
    prompt = str(prompt)
    user_input = input(prompt)
    new_lines = prompt.count("\n")
    for i in range(new_lines):
        delete_last_line()
    return user_input


if __name__ == "__main__":
    # Test the utility. This will not work by default in PyCharm or similar IDEs, where you must check the box to
    # emulate a terminal in the run window.
    require_input_and_clear("This is a long prompt.\nIt has multiple lines.\nDoes it still work?")
