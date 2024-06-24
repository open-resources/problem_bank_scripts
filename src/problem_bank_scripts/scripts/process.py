# Author: Firas Moosvi
# Date: 2021-05-09

import argparse
import os
import pathlib
import shutil

from ..problem_bank_scripts import process_question_md, process_question_pl


def _bool(v: str | bool):
    if isinstance(v, bool):
        return v

    v = v.lower()

    if v in {"yes", "true", "t", "y", "1"}:
        return True
    elif v in {"no", "false", "f", "n", "0"}:
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")

_base_args = {"type": _bool, "action": "store", "default": False, "metavar": "<bool>"}

def main():
    parser = argparse.ArgumentParser(
        description="Processes all questions.",
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("source_root", action="store", help="Root of all the md source files.")
    parser.add_argument("--instructor", help="Exports md version of question.", **_base_args)
    parser.add_argument("--public", help="Exports md version of question with the answers removed.", **_base_args)
    parser.add_argument("--prairielearn", help="Exports info.json, server.py, and question.html..", **_base_args)
    
    args = parser.parse_args()

    source_root = pathlib.Path().joinpath(args.source_root).resolve()

    if not source_root.exists():
        raise FileNotFoundError(f"Directory does not exist: {source_root}")

    if not source_root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {source_root}")

    questions = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if file.endswith(".md"):
                questions.append(os.path.join(root, file))

    excs = []

    # Read Question Files
    for source_filepath in questions:
        try:
            print(source_filepath)
            if args.instructor:
                process_question_md(source_filepath, instructor=True)

            if args.public:
                process_question_md(source_filepath, instructor=False)

            if args.prairielearn:
                process_question_pl(source_filepath)

        except Exception as e:
            e.add_note(f"Error in processing question: {source_filepath}")
            # print(f"There is an error in this problem: \n\t- File path: {source_filepath}\n\t- Error: {e}")
            # raise e
            excs.append(e)

    if excs:
        raise ExceptionGroup("Errors in processing questions:", excs)

    try:
        # Copy over the html_questions directory into output/prairielearn
        html_source = source_root.parent / "html_questions"
        target = source_root.parent / "output/prairielearn/html_questions"

        shutil.copytree(html_source, target, dirs_exist_ok=True)
    except FileNotFoundError as e:
        print(e)
        print("Skipping the copying of html sources; directories not correct.")


if __name__ == "__main__":
    main()
