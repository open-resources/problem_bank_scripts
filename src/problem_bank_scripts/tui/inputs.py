import questionary


def is_int(s: str) -> bool:
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


def validate_int(text: str):
    return True if is_int(text) else "Please enter an integer."


def ask_int(question: str, default: int | str = "") -> int:
    return int(questionary.text(question, validate=validate_int, default=str(default)).ask())
