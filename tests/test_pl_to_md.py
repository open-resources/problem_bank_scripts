from __future__ import annotations
import filecmp
import pathlib
import tempfile

import pytest

from problem_bank_scripts import pl_to_md

# Generate a list of all problems in the test problems directory
files = sorted(
    [
        file.name
        for file in pathlib.Path(
            "tests/test_question_templates/question_expected_outputs/prairielearn"
        ).iterdir()
        if file.name != ".DS_Store"
    ]
)


@pytest.mark.parametrize(
    "question",
    [file for file in files],
)
def test_pl_to_md(paths: dict[str, pathlib.Path], question: str):
    """Tests the ``pl_to_md()`` function

    Args:
        paths (dict): set by the fixture paths()
        question (str): the name of the question to test, set by the parametrize decorator
    """
    outputPath = paths["returnOutputDest"].joinpath(question)
    comparePath = paths["returnCompareDest"].joinpath(question)
    baseFile = paths["compareDest"].joinpath("prairielearn", f"{question}")
    folder = question
    pl_to_md(baseFile, outputPath, f"{question}.md")

    for file in sorted(comparePath.joinpath(f"{folder}/").glob("**/*")):
        isFile = file.is_file()
        hiddenFile = not file.name.startswith(".")
        assetFile = file.name == "question.html" or not file.name.endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".html", ".DS_Store")
        )
        excludedFile = False  # Leave this as false for now, but we may want to add a way to exclude files from the comparison

        print(hiddenFile, ~(hiddenFile))

        # TODO: Find a way to separately test info.json files
        infoJSON = not file.name.endswith("info.json")

        if isFile and hiddenFile and assetFile and excludedFile and infoJSON:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)

            try:
                filecmp.cmp(file, outputPath / file.relative_to(comparePath))
            except FileNotFoundError:
                print(
                    file,
                    folder,
                    outputFolder,
                    outputPath / file.relative_to(comparePath),
                )

            assert filecmp.cmp(
                file, outputPath / file.relative_to(comparePath)
            ), f"File: {'/'.join(file.parts[-2:])} did not match with expected output."


def test_question_exists_validation():
    with pytest.raises(FileNotFoundError):
        pl_to_md("fake", "fake", "fake.md")


def test_question_path_not_dir_validation():
    with pytest.raises(NotADirectoryError):
        pl_to_md(__file__, "fake", "fake.md")


def test_output_path_not_dir_validation():
    with pytest.raises(NotADirectoryError):
        pl_to_md(pathlib.Path(__file__).parent, __file__, "fake.md")


def test_output_path_warns_exists():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.warns(UserWarning), pytest.raises(FileNotFoundError): # we want to raise the error, but also check that the warning is emitted first
            pl_to_md(pathlib.Path(__file__).parent, pathlib.Path(tmpdirname), "fake.md")
