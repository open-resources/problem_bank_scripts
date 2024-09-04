import json
import pathlib

import fastjsonschema
import pytest


@pytest.fixture(scope="session")
def paths():
    """Sets the paths of where to find inputs, generated outputs, and expected outputs.

    Returns:
        Nothing, it's a fixture that is run before every test.
    """
    return {
        "inputDest": pathlib.Path("tests/test_question_templates/question_inputs/"),
        "outputDest": pathlib.Path("tests/test_question_templates/question_generated_outputs/"),
        "compareDest": pathlib.Path("tests/test_question_templates/question_expected_outputs/"),
        "returnCompareDest": pathlib.Path("tests/test_question_templates/question_return_expected_outputs/"),
        "returnOutputDest": pathlib.Path("tests/test_question_templates/question_return_generated_outputs/"),
    }


@pytest.fixture(scope="session")
def validate_info_json():
    """Generates a schema validator for info.json files.

    Returns:
        Nothing, it's a fixture that is run before every test.
    """
    with open("tests/infoSchema.json") as file:
        return fastjsonschema.compile(json.load(file))

@pytest.fixture(scope="session", autouse=True)
def monkeypatch_prairielearn():
    """Monkeypatches the prairielearn module into sys.modules to make it accessible."""

    import sys

    from problem_bank_scripts import prairielearn
    sys.modules["prairielearn"] = prairielearn