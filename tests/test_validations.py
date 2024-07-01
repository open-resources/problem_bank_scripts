from __future__ import annotations

import pytest
import sympy as sp

from problem_bank_scripts import ValidationError, process_symbolic_input, validate_multiple_choice
from problem_bank_scripts._vendored import python_helper_sympy as phs


def test_validate_multiple_choice_valid_has_correct_answer():
    """Tests the `validate_multiple_choice()` function with valid input."""

    parsed_question = {
        "header": {
            "part1": {
                "pl-customizations": {
                    "weight": 1,
                    "fixed-order": True,
                }
            }
        }
    }
    data_dict = {
        "params": {
            "part1": {
                "ans1": {"value": "Answer", "correct": True, "feedback": "Feedback"},
                "ans2": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans3": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "value": 1,
            }
        }
    }

    assert validate_multiple_choice("part1", parsed_question, data_dict) is True


@pytest.mark.parametrize("value", ["random", "correct"])
def test_validate_multiple_choice_valid_none_of_the_above(value: str):
    """Tests the `validate_multiple_choice()` function with valid input.

    Args:
        value (str): The value of the "none-of-the-above" key in the parsed question.
    """

    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1, "fixed-order": True, "none-of-the-above": value}}}
    }
    data_dict = {
        "params": {
            "part1": {
                "ans1": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans2": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans3": {"value": "Answer", "correct": False, "feedback": "Feedback"},
            }
        }
    }

    assert validate_multiple_choice("part1", parsed_question, data_dict) is True


def test_validate_multiple_choice_valid_has_truthy_non_bool_correct_answer():
    """Tests the `validate_multiple_choice()` function with valid input."""

    parsed_question = {
        "header": {
            "part1": {
                "pl-customizations": {
                    "weight": 1,
                    "fixed-order": True,
                }
            }
        }
    }
    data_dict = {
        "params": {
            "part1": {
                "ans1": {"value": "Answer", "correct": "True", "feedback": "Feedback"},
                "ans2": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans3": {"value": "Answer", "correct": False, "feedback": "Feedback"},
            }
        }
    }
    with pytest.warns(SyntaxWarning):
        assert validate_multiple_choice("part1", parsed_question, data_dict) is True


def test_validate_multiple_choice_invalid_has_falsy_non_bool_correct_answer():
    """Tests the `validate_multiple_choice()` function with valid input."""

    parsed_question = {
        "header": {
            "part1": {
                "pl-customizations": {
                    "weight": 1,
                    "fixed-order": True,
                }
            }
        }
    }
    data_dict = {
        "params": {
            "part1": {
                "ans1": {"value": "Answer", "correct": "", "feedback": "Feedback"},
                "ans2": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans3": {"value": "Answer", "correct": False, "feedback": "Feedback"},
            }
        }
    }
    with pytest.warns(SyntaxWarning):
        assert validate_multiple_choice("part1", parsed_question, data_dict) is False


def test_validate_multiple_choice_invalid_has_non_json_compatible_value_for_correct():
    """Tests the `validate_multiple_choice()` function with valid input."""

    parsed_question = {
        "header": {
            "part1": {
                "pl-customizations": {
                    "weight": 1,
                    "fixed-order": True,
                }
            }
        }
    }
    data_dict = {
        "params": {
            "part1": {
                "ans1": {"value": "Answer", "correct": 1j, "feedback": "Feedback"},
                "ans2": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans3": {"value": "Answer", "correct": False, "feedback": "Feedback"},
            }
        }
    }
    with pytest.raises(ValidationError, match=r"Object of type 'complex'.*"):
        validate_multiple_choice("part1", parsed_question, data_dict)


def test_validate_multiple_choice_invalid_none_of_the_above_unset():
    """Tests the `validate_multiple_choice()` function with valid input.

    Args:
        value (str): The value of the "none-of-the-above" key in the parsed question.
    """

    parsed_question = {
        "header": {
            "part1": {
                "pl-customizations": {
                    "weight": 1,
                    "fixed-order": True,
                }
            }
        }
    }
    data_dict = {
        "params": {
            "part1": {
                "ans1": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans2": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans3": {"value": "Answer", "correct": False, "feedback": "Feedback"},
            }
        }
    }

    assert validate_multiple_choice("part1", parsed_question, data_dict) is False


@pytest.mark.parametrize("value", ["false", "incorrect"])
def test_validate_multiple_choice_invalid_none_of_the_above_set(value: str):
    """Tests the `validate_multiple_choice()` function with valid input.

    Args:
        value (str): The value of the "none-of-the-above" key in the parsed question.
    """

    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1, "fixed-order": True, "none-of-the-above": value}}}
    }
    data_dict = {
        "params": {
            "part1": {
                "ans1": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans2": {"value": "Answer", "correct": False, "feedback": "Feedback"},
                "ans3": {"value": "Answer", "correct": False, "feedback": "Feedback"},
            }
        }
    }

    assert validate_multiple_choice("part1", parsed_question, data_dict) is False

_x = sp.symbols("x")
_N = sp.symbols("N", cls=sp.Function)

@pytest.mark.parametrize(
    "answer",
    [
        pytest.param(_x, id="x"),
        pytest.param(5*_x, id="5x"),
        pytest.param(5*_x/2, id="5x/2"),
        pytest.param(2*_x/5, id="2x/5"),
        pytest.param(5*_x+1, id="5x+1"),
        pytest.param(_N(5*_x), id="N(5x)"),
        pytest.param(_N(5*_x+1), id="N(5x+1)"),
        pytest.param(_N(5*_x)+1, id="N(5x)+1"),
        pytest.param(5*_N(_x), id="5N(x)"),
        pytest.param(5*_N(_x)+1, id="5N(x)+1"),
    ],
)
def test_validate_symbolic_input_valid_sympy_object(answer:sp.Expr):
    """Tests the `validate_symbolic_input()` function with valid input."""

    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1}}},
        "body_parts_split": {"part1": {"content": "..."}},
    }
    data_dict = {"params": {"part1": {"correct_ans": phs.sympy_to_json(answer)}}}

    assert isinstance(process_symbolic_input("part1", parsed_question, data_dict), str)


@pytest.mark.parametrize("answer", ["x", "5x", "5x/2", "5/2x", "5/(2x)", "(5/2)x", "5*x", "5 * x", "N(x)", "N(x) + 1", "5N(x)", "N(5x)"])
def test_validate_symbolic_input_valid_string(answer: str, subtests):
    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1, "variables": "x", "functions": "N"}}},
        "body_parts_split": {"part1": {"content": "..."}},
    }
    data_dict = {"params": {"part1": {}}}

    for location in ("pl-customizations", "params"):
        if location == "pl-customizations":
            parsed_question["header"]["part1"]["pl-customizations"]["correct-answer"] = answer
        else:
            data_dict["params"]["part1"] = {"correct_ans": answer}

        with subtests.test(correct_ans_location=location):
            assert isinstance(process_symbolic_input("part1", parsed_question, data_dict), str)

@pytest.mark.parametrize(
    "answer",
    [
        pytest.param(5.1*_x, id="5.1x"),
        pytest.param(5.1*_x+1, id="5.1x+1"),
        pytest.param(5*_x+1.1, id="5x+1.1"),
        pytest.param(5.1*_x+1.1, id="5.1x+1.1"),
        pytest.param(_N(5.1*_x), id="N(5.1x)"),
        pytest.param(_N(5.1*_x+1), id="N(5.1x+1)"),
        pytest.param(_N(5*_x+1.1), id="N(5x+1.1)"),
        pytest.param(_N(5.1*_x)+1, id="N(5.1x)+1"),
        pytest.param(_N(5*_x)+1.1, id="N(5x)+1.1"),
        pytest.param(_N(5.1*_x)+1.1, id="N(5.1x)+1.1"),
        pytest.param(5.1*_N(_x), id="5.1N(x)"),
        pytest.param(5.1*_N(_x)+1, id="5.1N(x)+1"),
        pytest.param(5*_N(_x)+1.1, id="5N(x)+1.1"),
        pytest.param(5.1*_N(_x)+1.1, id="5.1N(x)+1.1"),
    ],
)
def test_validate_symbolic_input_invalid_sympy_object(answer:sp.Expr):
    """Tests the `validate_symbolic_input()` function with valid input."""

    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1}}},
        "body_parts_split": {"part1": {"content": "..."}},
    }
    data_dict = {"params": {"part1": {"correct_ans": phs.sympy_to_json(answer)}}}

    with pytest.raises(ValidationError, match=r"The correct answer for part 'part1' contains the floating-point number "):
        process_symbolic_input("part1", parsed_question, data_dict)


@pytest.mark.parametrize("answer", ["5.1x", "5.1*x", "5.1 * x", "N(x) + 1.1", "5.1N(x)", "N(5.1x)"])
def test_validate_symbolic_input_invalid_string(answer: str, subtests):
    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1, "variables": "x", "functions": "N"}}},
        "body_parts_split": {"part1": {"content": "..."}},
    }
    data_dict = {"params": {"part1": {}}}

    for location in ("pl-customizations", "params"):
        if location == "pl-customizations":
            parsed_question["header"]["part1"]["pl-customizations"]["correct-answer"] = answer
        else:
            data_dict["params"]["part1"] = {"correct_ans": answer}

        with subtests.test(correct_ans_location=location):
            with pytest.raises(ValidationError, match=r"The correct answer for part 'part1' contains the floating-point number "):
                process_symbolic_input("part1", parsed_question, data_dict)
