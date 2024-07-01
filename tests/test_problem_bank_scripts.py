from __future__ import annotations

import filecmp
import json
import os
import pathlib

import fastjsonschema
import pytest

from problem_bank_scripts import process_question_md, process_question_pl, validate_multiple_choice


questions_dir = pathlib.Path(__file__).parent / "test_question_templates"

# Generate a list of all problems in the test problems directory
files = sorted(file.name for file in questions_dir.joinpath("question_inputs").iterdir() if file.name != ".DS_Store")


@pytest.fixture(scope="session")
def paths():
    """Sets the paths of where to find inputs, generated outputs, and expected outputs.

    Returns:
        Nothing, it's a fixture that is run before every test.
    """
    p = {
        "inputDest": questions_dir.joinpath("question_inputs"),
        "outputDest": questions_dir.joinpath("question_generated_outputs"),
        "compareDest": questions_dir.joinpath("question_expected_outputs"),
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


_tested_questions = set()


def run_prairie_learn_generator(paths: dict[str, pathlib.Path], question: str, devmode: bool):
    """Helper function that runs the PrairieLearn generator on a question.

    This allows us to deduplicate the code for running the generator.

    Args:
        paths (dict): definition of the output and input paths
        question (str): the name of the question to test, set by the parametrize decorator
        devmode (bool): whether to run the generator in devmode
    """
    if (question, devmode) in _tested_questions:
        return  # don't parse the same question twice
    _tested_questions.add((question, devmode))
    outputPath = paths["outputDest"].joinpath(f"prairielearn{'-dev' if devmode else ''}/")

    baseFile = paths["inputDest"] / question / f"{question}.md"
    folder = baseFile.parent.stem
    outputFolder = outputPath.joinpath(folder)
    process_question_pl(baseFile, outputFolder.joinpath(baseFile.name), devmode)


@pytest.mark.parametrize(
    ("question", "devmode"),
    [
        pytest.param(file, dev, id=(f"dev-{file}" if dev else f"nodev-{file}"))
        for file in files
        for dev in [False, True]
    ],
)
def test_prairie_learn(paths: dict[str, pathlib.Path], question: str, devmode: bool):
    """Tests the PrairieLearn `process_question_pl()`

    Args:
        paths (dict): set by the fixture paths()
        question (str): the name of the question to test, set by the parametrize decorator
        devmode (bool): whether to run the generator in devmode
    """
    run_prairie_learn_generator(paths, question, devmode)
    outputPath = paths["outputDest"].joinpath(f"prairielearn{'-dev' if devmode else ''}/")
    comparePath = paths["compareDest"].joinpath(f"prairielearn{'-dev' if devmode else ''}/")
    baseFile = paths["inputDest"].joinpath(f"{question}/{question}.md")
    folder = baseFile.parent.stem

    for file in sorted(comparePath.joinpath(f"{folder}/").glob("**/*")):
        isFile = os.path.isfile(file)
        hiddenFile = not file.name.startswith(".")
        assetFile = file.name == "question.html" or not file.name.endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".html", ".DS_Store")
        )

        infoJSON = not file.name.endswith("info.json")

        if isFile and hiddenFile and assetFile and infoJSON:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)

            try:
                filecmp.cmp(file, outputPath / file.relative_to(comparePath))
            except FileNotFoundError:
                print(file, folder, outputFolder, outputPath / file.relative_to(comparePath))

            assert filecmp.cmp(
                file, outputPath / file.relative_to(comparePath)
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."


@pytest.mark.parametrize(
    ("question", "devmode"),
    [
        pytest.param(file, dev, id=(f"nodev-{file}" if dev else f"dev-{file}"))
        for file in files
        for dev in [False, True]
    ],
)
def test_info_json(paths: dict[str, pathlib.Path], question: str, devmode: bool, validate_info_json):
    """Tests the PrairieLearn `process_question_pl()` info.json file

    Args:
        paths (dict): set by the fixture paths()
        question (str): the name of the question to test, set by the parametrize decorator
        devmode (bool): whether to run the generator in devmode
    """
    run_prairie_learn_generator(paths, question, devmode)
    output_info_json = paths["outputDest"].joinpath(f"prairielearn{'-dev' if devmode else ''}/{question}/info.json")
    compare_info_json = paths["compareDest"].joinpath(f"prairielearn{'-dev' if devmode else ''}/{question}/info.json")
    generated_json = json.loads(output_info_json.read_bytes())
    expected_json = json.loads(compare_info_json.read_bytes())
    validate_info_json(generated_json)
    del generated_json["uuid"]  # uuid is semi-randomly generated, so we can't compare reliably it
    del expected_json["uuid"]
    for key in expected_json:
        generated = generated_json[key]
        if isinstance(generated, list):
            generated = sorted(generated)
        expected = expected_json[key]
        if isinstance(expected, list):
            expected = sorted(expected)
        assert expected == generated, f"info.json key {key} for {question} did not match with expected output."


@pytest.mark.parametrize("question", files)
def test_public(paths: dict[str, pathlib.Path], question: str):
    """Tests the PrairieLearn `process_question_md()`

    Args:
        paths (dict): set by the fixture paths()
        question (str): the name of the question to test, set by the parametrize decorator
    """
    outputPath = paths["outputDest"].joinpath("public/")
    comparePath = paths["compareDest"].joinpath("public/")

    baseFile = paths["inputDest"] / question / f"{question}.md"
    folder = baseFile.parent.stem
    outputFolder = outputPath.joinpath(folder)
    process_question_md(baseFile, outputFolder.joinpath(baseFile.name), instructor=False)

    for file in sorted(comparePath.joinpath(f"{folder}/").glob("**/*")):
        isFile = os.path.isfile(file)
        notHiddenFile = not file.name.startswith(".")
        notImageFile = not file.name.endswith(".png")
        if isFile and notHiddenFile and notImageFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(
                file, outputPath / file.relative_to(comparePath), shallow=False
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."


@pytest.mark.parametrize("question", files)
def test_instructor(paths: dict[str, pathlib.Path], question: str):
    """Tests the PrairieLearn `process_question_md(instructor=True)`

    Args:
        paths (dict): set by the fixture paths()
        question (str): the name of the question to test, set by the parametrize decorator
    """
    outputPath = paths["outputDest"].joinpath(
        "instructor/"
    )  # the path to where the newly generated file will be stored
    comparePath = paths["compareDest"].joinpath(
        "instructor/"
    )  # the path to where the existing files to be compared are stored

    baseFile = paths["inputDest"] / question / f"{question}.md"
    folder = baseFile.parent.stem
    outputFolder = outputPath.joinpath(folder)
    process_question_md(baseFile, outputFolder.joinpath(baseFile.name), instructor=True)

    for file in sorted(comparePath.joinpath(f"{folder}/").glob("**/*")):
        isFile = os.path.isfile(file)
        notHiddenFile = not file.name.startswith(".")
        notImageFile = not file.name.endswith(".png")

        if isFile and notHiddenFile and notImageFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(
                file, outputPath / file.relative_to(comparePath), shallow=False
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."
