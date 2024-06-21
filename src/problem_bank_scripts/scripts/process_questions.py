# Author: Firas Moosvi
# Date: 2021-05-09

"""Processes all questions.

Usage:
    process.py [--instructor=<bool>] [--public=<bool>] [--prairielearn=<bool>] <source_root>

Arguments:
    source_root                Root of all the md source files.

Options:
    --instructor=<bool>        Exports md version of question.
    --public=<bool>            Exports md version of question with the answers removed.
    --prairielearn=<bool>      Exports info.json, server.py, and question.html.
"""

import argparse
import pathlib
import os
import shutil
from .. import problem_bank_scripts as pbs

def main():
    parser = argparse.ArgumentParser(description="Processes all questions.")
    parser.add_argument("--instructor", type=bool, action="store", default=False, help="Exports md version of question.", metavar="<bool>")
    parser.add_argument("--public", type=bool, action="store", default=False, help="Exports md version of question with the answers removed.", metavar="<bool>")
    parser.add_argument("--prairielearn", type=bool, action="store", default=False, help="Exports info.json, server.py, and question.html.", metavar="<bool>")
    parser.add_argument("source_root", type=str, action="store", help="Root of all the md source files.")
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
                questions.append(os.path.join(root,file))

    excs = []

    # Read Question Files
    for source_filepath in questions:
        try:
            print(source_filepath)
            if args.instructor:
                pbs.process_question_md(source_filepath, instructor=True)

            if args.public:
                pbs.process_question_md(source_filepath, instructor=False)

            if args.prairielearn:
                pbs.process_question_pl(source_filepath)

        except Exception as e:
            e.add_note(f"Error in processing question: {source_filepath}")
            # print(f"There is an error in this problem: \n\t- File path: {source_filepath}\n\t- Error: {e}")
            # raise e
            excs.append(e)

    if excs:
        raise ExceptionGroup("Errors in processing questions:", excs)

    try:
        # Copy over the html_questions directory into output/prairielearn
        html_source = source_root.parent / 'html_questions'
        target = source_root.parent / 'output/prairielearn/html_questions'

        shutil.copytree(html_source, target,dirs_exist_ok=True)
    except FileNotFoundError as e:
        print(e)
        print("Skipping the copying of html sources; directories not correct.")
        
if __name__ == '__main__':
    main()
