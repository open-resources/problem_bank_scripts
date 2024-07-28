import random


def generate_given_choices(options: list[str], answer: str | None = None):
    if answer:
        answer = answer.strip().lower()
    choices = [
        {
            "value": f'"{option}"',
            "correct": False,
            "feedback": '"Try again please!"',
        }
        for option in options
    ]
    # TODO: add actual choices
    correct = random.randrange(0, len(choices))
    if answer:
        for i, option in enumerate(options):
            first_letter = option.strip()[0].lower()
            if answer.startswith(first_letter):
                correct = i
                break
            if option in answer:
                correct = i
    choices[correct]["correct"] = True
    choices[correct]["feedback"] = '"Correct!"'
    return choices


def generate_yes_no_choices(answer: str | None = None):
    return generate_given_choices(["Yes", "No"], answer)


def generate_true_false_choices(answer: str | None = None):
    wrong_feedback = '"Try again please!"'  #  if not answer else answer
    # Do I have access to solutions here?
    choices = [
        {"value": '"True"', "correct": False, "feedback": wrong_feedback},
        {"value": '"False"', "correct": False, "feedback": wrong_feedback},
    ]
    correct = random.randrange(0, len(choices))
    if answer:
        answer = answer.strip().lower()
        if answer[0] == ("t"):
            correct = 0
        elif answer[0] == ("f"):
            correct = 1
        elif "true" in answer:
            correct = 0
        elif "false" in answer:
            correct = 1
    choices[correct]["correct"] = True
    choices[correct]["feedback"] = '"Correct!"'
    return choices
