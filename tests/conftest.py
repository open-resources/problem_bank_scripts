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
    p = {
        "inputDest": pathlib.Path("tests/test_question_templates/question_inputs/"),
        "outputDest": pathlib.Path(
            "tests/test_question_templates/question_generated_outputs/"
        ),
        "compareDest": pathlib.Path(
            "tests/test_question_templates/question_expected_outputs/"
        ),
        "returnCompareDest": pathlib.Path(
            "tests/test_question_templates/question_return_expected_outputs/"
        ),
        "returnOutputDest": pathlib.Path(
            "tests/test_question_templates/question_return_generated_outputs/"
        ),
    }
    return p


@pytest.fixture(scope="session")
def validate_info_json():
    """Generates a schema validator for info.json files.

    Returns:
        Nothing, it's a fixture that is run before every test.
    """
    with open("tests/infoSchema.json") as file:
        schema = fastjsonschema.compile(json.load(file))
    return schema