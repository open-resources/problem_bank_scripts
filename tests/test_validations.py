from __future__ import annotations

import pytest
import sympy as sp

from problem_bank_scripts import ValidationError, process_symbolic_input, process_workspace, validate_multiple_choice
from problem_bank_scripts._vendored import python_helper_sympy as phs


def test_validate_multiple_choice_valid_has_correct_answer():
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
        pytest.param(5 * _x, id="5x"),
        pytest.param(5 * _x / 2, id="5x/2"),
        pytest.param(2 * _x / 5, id="2x/5"),
        pytest.param(5 * _x + 1, id="5x+1"),
        pytest.param(_N(5 * _x), id="N(5x)"),
        pytest.param(_N(5 * _x + 1), id="N(5x+1)"),
        pytest.param(_N(5 * _x) + 1, id="N(5x)+1"),
        pytest.param(5 * _N(_x), id="5N(x)"),
        pytest.param(5 * _N(_x) + 1, id="5N(x)+1"),
    ],
)
def test_validate_symbolic_input_valid_sympy_object(answer: sp.Expr):
    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1}}},
        "body_parts_split": {"part1": {"content": "..."}},
    }
    data_dict = {"correct_answers": {"part1_ans": phs.sympy_to_json(answer)}}

    assert isinstance(process_symbolic_input("part1", parsed_question, data_dict), str)


@pytest.mark.parametrize(
    "answer", ["x", "5x", "5x/2", "5/2x", "5/(2x)", "(5/2)x", "5*x", "5 * x", "N(x)", "N(x) + 1", "5N(x)", "N(5x)"]
)
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
        pytest.param(5.1 * _x, id="5.1x"),
        pytest.param(5.1 * _x + 1, id="5.1x+1"),
        pytest.param(5 * _x + 1.1, id="5x+1.1"),
        pytest.param(5.1 * _x + 1.1, id="5.1x+1.1"),
        pytest.param(_N(5.1 * _x), id="N(5.1x)"),
        pytest.param(_N(5.1 * _x + 1), id="N(5.1x+1)"),
        pytest.param(_N(5 * _x + 1.1), id="N(5x+1.1)"),
        pytest.param(_N(5.1 * _x) + 1, id="N(5.1x)+1"),
        pytest.param(_N(5 * _x) + 1.1, id="N(5x)+1.1"),
        pytest.param(_N(5.1 * _x) + 1.1, id="N(5.1x)+1.1"),
        pytest.param(5.1 * _N(_x), id="5.1N(x)"),
        pytest.param(5.1 * _N(_x) + 1, id="5.1N(x)+1"),
        pytest.param(5 * _N(_x) + 1.1, id="5N(x)+1.1"),
        pytest.param(5.1 * _N(_x) + 1.1, id="5.1N(x)+1.1"),
    ],
)
def test_validate_symbolic_input_invalid_sympy_object(answer: sp.Expr):
    parsed_question = {
        "header": {"part1": {"pl-customizations": {"weight": 1}}},
        "body_parts_split": {"part1": {"content": "..."}},
    }
    data_dict = {"correct_answers": {"part1_ans": phs.sympy_to_json(answer)}}

    with pytest.raises(
        ValidationError, match=r"The correct answer for part 'part1' contains the floating-point number "
    ):
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
            with pytest.raises(
                ValidationError, match=r"The correct answer for part 'part1' contains the floating-point number "
            ):
                process_symbolic_input("part1", parsed_question, data_dict)


def test_validate_workspace_valid_config():
    parsed_question = {
        "header": {
            "workspaceOptions": {
                "image": "prairielearn/workspace-rstudio",
                "port": 3939,
                "args": "",
                "rewriteUrl": False,
                "home": "/home/rstudio/workspace",
                "gradedFiles": ["student.R"],
                "enableNetworking": False,
                "environment": {"key": "value"},
            },
            "part1": {"pl-customizations": {}},
        },
        "body_parts_split": {"part1": {"content": "..."}},
    }

    assert isinstance(process_workspace("part1", parsed_question, {}), str)


@pytest.mark.parametrize("key", ["rewriteUrl", "args", "gradedFiles", "enableNetworking", "environment"])
def test_validate_workspace_missing_optional_key(key: str):
    parsed_question = {
        "header": {
            "workspaceOptions": {
                "image": "prairielearn/workspace-rstudio",
                "port": 3939,
                "home": "/home/rstudio/workspace",
                "rewriteUrl": False,
                "args": "",
                "gradedFiles": ["student.R"],
                "enableNetworking": False,
                "environment": {"key": "value"},
            },
            "part1": {"pl-customizations": {}},
        },
        "body_parts_split": {"part1": {"content": "..."}},
    }

    del parsed_question["header"]["workspaceOptions"][key]

    assert isinstance(process_workspace("part1", parsed_question, {}), str)


@pytest.mark.parametrize("key", ["image", "port", "home"])
def test_validate_workspace_missing_required_key(key: str):
    parsed_question = {
        "header": {
            "workspaceOptions": {
                "image": "prairielearn/workspace-rstudio",
                "port": 3939,
                "args": "",
                "rewriteUrl": False,
                "home": "/home/rstudio/workspace",
                "gradedFiles": ["student.R"],
                "enableNetworking": False,
                "environment": {"key": "value"},
            },
            "part1": {"pl-customizations": {}},
        },
        "body_parts_split": {"part1": {"content": "..."}},
    }

    del parsed_question["header"]["workspaceOptions"][key]

    with pytest.raises(
        ValidationError, match=r"^\[part 'part1'\]: workspaceOptions must contain image, port, and home keys$"
    ):
        process_workspace("part1", parsed_question, {})


def test_validate_workspace_missing_config():
    parsed_question = {
        "header": {"part1": {"pl-customizations": {}}},
        "body_parts_split": {"part1": {"content": "..."}},
    }

    with pytest.raises(
        ValidationError,
        match=r"^'workspaceOptions' object not found in the question frontmatter, but part 'part1' is a workspace question$",
    ):
        process_workspace("part1", parsed_question, {})


def test_validate_workspace_pl_customizations_present():
    parsed_question = {"header": {"part1": {"pl-customizations": {"weight": 1}}}}

    with pytest.raises(
        ValidationError, match=r"^\[part 'part1'\]: pl-customizations are not supported for workspace questions$"
    ):
        process_workspace("part1", parsed_question, {})


@pytest.mark.parametrize(
    ("key", "value", "msg"),
    [
        pytest.param(
            "image", 1, r"^\[part 'part1'\]: workspaceOptions.image must be a string, got 1 instead$", id="image"
        ),
        pytest.param(
            "port", "1", r"^\[part 'part1'\]: workspaceOptions.port must be an integer, got '1' instead$", id="port"
        ),
        pytest.param(
            "home", 1, r"^\[part 'part1'\]: workspaceOptions.home must be a string, got 1 instead$", id="home"
        ),
        pytest.param(
            "gradedFiles",
            1,
            r"^\[part 'part1'\]: workspaceOptions.gradedFiles must be a list of strings, got 1 instead$",
            id="gradedFiles:wrong-outer-type",
        ),
        pytest.param(
            "gradedFiles",
            [1],
            r"^\[part 'part1'\]: workspaceOptions.gradedFiles must be a list of strings, got \[1\] instead$",
            id="gradedFiles:wrong-inner-type",
        ),
        pytest.param(
            "args", 1, r"^\[part 'part1'\]: workspaceOptions.args must be a string, got 1 instead$", id="args"
        ),
        pytest.param(
            "rewriteUrl",
            1,
            r"^\[part 'part1'\]: workspaceOptions.rewriteUrl must be a boolean, got 1 instead$",
            id="rewriteUrl",
        ),
        pytest.param(
            "enableNetworking",
            1,
            r"^\[part 'part1'\]: workspaceOptions.enableNetworking must be a boolean, got 1 instead$",
            id="enableNetworking",
        ),
        pytest.param(
            "environment",
            1,
            r"^\[part 'part1'\]: workspaceOptions.environment must be a dictionary of strings, got 1 instead$",
            id="environment:wrong-outer-type",
        ),
        pytest.param(
            "environment",
            {"a": 1},
            r"^\[part 'part1'\]: workspaceOptions.environment must be a dictionary of strings, got {'a': 1} instead$",
            id="environment:wrong-inner-type",
        ),
    ],
)
def test_validate_workspace_invalid_config_value(key: str, value, msg: str):
    parsed_question = {
        "header": {
            "workspaceOptions": {
                "image": "prairielearn/workspace-rstudio",
                "port": 3939,
                "args": "",
                "rewriteUrl": False,
                "home": "/home/rstudio/workspace",
                "gradedFiles": ["student.R"],
                "enableNetworking": False,
                "environment": {"key": "value"},
            },
            "part1": {"pl-customizations": {}},
        },
        "body_parts_split": {"part1": {"content": "..."}},
    }

    parsed_question["header"]["workspaceOptions"][key] = value

    with pytest.raises(ValidationError, match=msg):
        process_workspace("part1", parsed_question, {})


def test_validate_workspace_warn_enable_networking_config_true():
    parsed_question = {
        "header": {
            "workspaceOptions": {
                "image": "prairielearn/workspace-rstudio",
                "port": 3939,
                "home": "/home/rstudio/workspace",
                "enableNetworking": True,
            },
            "part1": {"pl-customizations": {}},
        },
        "body_parts_split": {"part1": {"content": "..."}},
    }

    with pytest.warns(
        UserWarning,
        match=r"^\[part 'part1'\]: workspaceOptions.enableNetworking is set to True, which is not recommended for security reasons$",
    ):
        process_workspace("part1", parsed_question, {})


def test_validate_workspace_invalid_config_extra_key():
    parsed_question = {
        "header": {
            "workspaceOptions": {
                "image": "prairielearn/workspace-rstudio",
                "port": 3939,
                "args": "",
                "rewriteUrl": False,
                "home": "/home/rstudio/workspace",
                "gradedFiles": ["student.R"],
                "enableNetworking": False,
                "Environment": {"key": "value"},
                "extra1": "key",
                "extra2": "key",
            },
            "part1": {"pl-customizations": {}},
        },
        "body_parts_split": {"part1": {"content": "..."}},
    }

    with pytest.raises(
        ValidationError, match=r"^\[part 'part1'\]: workspaceOptions contains one or more unknown keys:"
    ):
        process_workspace("part1", parsed_question, {})
