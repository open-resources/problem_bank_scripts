from __future__ import annotations

# python >= 3.8 doesn't support subscripting builtin collections

import filecmp
import os
import pathlib

import pandas as pd
import pytest

from problem_bank_scripts import __version__, process_question_pl, process_question_md


def test_version():
    assert __version__ == "0.5.0"


# TODO: excluding symbolic questions, needs to be fixed because of how sympy objects are handled
exclude_question = (
    "q07a_symbolic-input",
    "q07b_symbolic-input",
)

# Generate a list of all problems in the test problems directory
files = sorted(
    [
        file.name
        for file in pathlib.Path(
            "tests/test_question_templates/question_inputs/"
        ).iterdir()
    ]
)

files = [f for f in files if f != '.DS_Store']

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


@pytest.mark.parametrize(
    "question",
    [
        pytest.param(
            file,
            id=file,
            marks=([pytest.mark.xfail(reason="Problem specified in the `exclude_question` list")] if file in exclude_question else []),
        )
        for file in files
    ],
)
def test_prairie_learn(paths: dict[str, pathlib.Path], question: str):
    """Tests the PrairieLearn `process_question_pl()`

    Args:
        paths (dict): set by the fixture paths()
    """
    if question != "q13_file-editor-input":
        return
    outputPath = paths["outputDest"].joinpath("prairielearn/")
    comparePath = paths["compareDest"].joinpath("prairielearn/")

    baseFile = paths["inputDest"] / question / f"{question}.md"
    folder = baseFile.parent.stem
    outputFolder = outputPath.joinpath(folder)
    process_question_pl(baseFile, outputFolder.joinpath(baseFile.name))

    for file in sorted(comparePath.joinpath(f"{folder}/").glob("**/*")):
        isFile = os.path.isfile(file)
        hiddenFile = not file.name.startswith(".")
        assetFile = not file.name.endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".html", ".DS_Store")
        )
        excludedFile = not file.parent.name in exclude_question

        print(hiddenFile, ~(hiddenFile))

        # TODO: Find a way to separately test info.json files
        infoJSON = not file.name.endswith("info.json")

        if isFile and hiddenFile and assetFile and excludedFile and infoJSON:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)

            try:
                filecmp.cmp(file, str(file).replace(str(comparePath), str(outputPath)))
            except FileNotFoundError:
                print(file, folder, outputFolder, str(file).replace(str(comparePath), str(outputPath)))

            assert filecmp.cmp(
                file, str(file).replace(str(comparePath), str(outputPath))
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."


@pytest.mark.parametrize(
    "question",
    [
        pytest.param(
            file,
            id=file,
            marks=([pytest.mark.xfail(reason="Problem specified in the `exclude_question` list")] if file in exclude_question else []),
        )
        for file in files
    ],
)
def test_public(paths: dict[str, pathlib.Path], question: str):
    """Tests the PrairieLearn `process_question_md()`

    Args:
        paths (dict): set by the fixture paths()
    """
    outputPath = paths["outputDest"].joinpath("public/")
    comparePath = paths["compareDest"].joinpath("public/")

    baseFile = paths["inputDest"] / question / f"{question}.md"
    folder = baseFile.parent.stem
    outputFolder = outputPath.joinpath(folder)
    process_question_md(
        baseFile, outputFolder.joinpath(baseFile.name), instructor=False
    )

    for file in sorted(comparePath.joinpath(f"{folder}/").glob("**/*")):
        isFile = os.path.isfile(file)
        notHiddenFile = not file.name.startswith(".")
        notImageFile = not file.name.endswith(".png")
        if isFile and notHiddenFile and notImageFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(
                file, outputFolder.joinpath(file.name), shallow=False
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."


@pytest.mark.parametrize(
    "question",
    [
        pytest.param(
            file,
            id=file,
            marks=([pytest.mark.xfail(reason="Problem specified in the `exclude_question` list")] if file in exclude_question else []),
        )
        for file in files
    ],
)
def test_instructor(paths: dict[str, pathlib.Path], question: str):
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

    baseFile = paths["inputDest"] / question / f"{question}.md"
    folder = baseFile.parent.stem
    outputFolder = outputPath.joinpath(folder)
    process_question_md(baseFile, outputFolder.joinpath(baseFile.name), instructor=True)

    for file in sorted(comparePath.joinpath(f"{folder}/").glob("**/*")):
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
