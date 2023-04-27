from problem_bank_scripts import __version__, process_question_pl, process_question_md
import pandas as pd
import pathlib
import filecmp
import os
import pytest


def test_version():
    assert __version__ == "0.4.8"


# TODO: excluding symbolic questions, needs to be fixed because of how sympy objects are handled
exclude_question = (
    "q07a_symbolic-input",
    "q07b_symbolic-input",
)


@pytest.fixture(scope="session")
def paths():
    """Sets the paths of where to find inputs, generated outputs, and expected outputs.

    Returns:
        Nothing, it's a fixture that is run before every test.
    """
    p = {
        "inputDest": pathlib.Path("tests/test_question_templates/question_inputs/"),
        "outputDest": pathlib.Path("tests/test_question_templates/question_generated_outputs/"),
        "compareDest": pathlib.Path("tests/test_question_templates/question_expected_outputs/"),
    }
    return p


def test_prairie_learn(paths):
    """Tests the PrairieLearn `process_question_pl()`

    Args:
        paths (dict): set by the fixture paths()
    """

    outputPath = paths["outputDest"].joinpath("prairielearn/")
    comparePath = paths["compareDest"].joinpath("prairielearn/")

    for file in sorted(paths["inputDest"].glob("**/*.md")):
        if file.name not in exclude_question:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            process_question_pl(file, outputFolder.joinpath(file.name))

    for file in sorted(comparePath.glob("**/*")):
        isFile = os.path.isfile(file)
        hiddenFile = not file.name.startswith(".")
        assetFile = not file.name.endswith((".png",".jpg",".jpeg",".gif",".html",".DS_Store"))
        excludedFile = not file.parent.name in exclude_question

        print(hiddenFile,~(hiddenFile))

        # TODO: Find a way to separately test info.json files
        infoJSON = not file.name.endswith("info.json")

        if isFile and hiddenFile and assetFile and excludedFile and infoJSON:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)

            try:
                filecmp.cmp(file, outputFolder.joinpath(file.name), shallow=False)
            except FileNotFoundError:
                print(file, folder, outputFolder,outputFolder.joinpath(file.name))

            assert filecmp.cmp(
                file, outputFolder.joinpath(file.name), shallow=False
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."


def test_public(paths):
    """Tests the PrairieLearn `process_question_md()`

    Args:
        paths (dict): set by the fixture paths()
    """
    outputPath = paths["outputDest"].joinpath("public/")
    comparePath = paths["compareDest"].joinpath("public/")

    for file in sorted(paths["inputDest"].glob("**/*.md")):
        if file.name not in exclude_question:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            process_question_md(file, outputFolder.joinpath(file.name), instructor=False)

    for file in sorted(comparePath.glob("**/*")):
        isFile = os.path.isfile(file)
        notHiddenFile = not file.name.startswith(".")
        notImageFile = not file.name.endswith(".png")
        if isFile and notHiddenFile and notImageFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(
                file, outputFolder.joinpath(file.name), shallow=False
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."


def test_instructor(paths):
    """Tests the PrairieLearn `process_question_md(instructor=True)`

    Args:
        paths (dict): set by the fixture paths()
    """
    outputPath = paths["outputDest"].joinpath(
        "instructor/"
    )  # the path to where the newly generated file will be stored
    comparePath = paths["compareDest"].joinpath(
        "instructor/"
    )  # the path to where the existing files to be compared are stored

    for file in sorted(paths["inputDest"].glob("**/*.md")):
        if file.name not in exclude_question:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            process_question_md(file, outputFolder.joinpath(file.name), instructor=True)

    for file in sorted(comparePath.glob("**/*")):
        isFile = os.path.isfile(file)
        notHiddenFile = not file.name.startswith(".")
        notImageFile = not file.name.endswith(".png")
        notExcludedFile = not (file.parent.name in exclude_question)

        if isFile and notHiddenFile and notImageFile and notExcludedFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(
                file, outputFolder.joinpath(file.name), shallow=False
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."
