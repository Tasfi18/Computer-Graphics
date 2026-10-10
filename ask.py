"""Small input helper shared by the interactive scripts."""
def ask_int(prompt, minimum=None):
    """Ask until the answer is a whole number (and at least `minimum`, if given)."""
    while True:
        answer = input(prompt).strip()
        try:
            value = int(answer)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Please enter a number of at least {minimum}.")
            continue
        return value
