import pytest

from problem_bank_scripts import __version__, validate_multiple_choice

def test_version():
    assert __version__ == "0.10.0"


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
        "header": {
            "part1": {
                "pl-customizations": {
                    "weight": 1,
                    "fixed-order": True,
                    "none-of-the-above": value
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
    with pytest.raises(TypeError, match=r"Object of type 'complex'.*"):
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
        "header": {
            "part1": {
                "pl-customizations": {
                    "weight": 1,
                    "fixed-order": True,
                    "none-of-the-above": value
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