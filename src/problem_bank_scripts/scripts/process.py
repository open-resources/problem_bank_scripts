# Author: Firas Moosvi
# Date: 2021-05-09

import argparse
import os
import pathlib
import shutil
import sys
from collections.abc import Sequence

from problem_bank_scripts import process_question_md, process_question_pl


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


def create_parser(subparsers: argparse._SubParsersAction | None) -> argparse.ArgumentParser:
    if subparsers is None:
        parser = argparse.ArgumentParser(
            description="Processes all questions.",
            allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    else:
        parser = subparsers.add_parser(
            "process",
            description="Processes all questions.",
            allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            help="Processes all questions.",
        )
    parser.add_argument("source_root", action="store", help="Root of all the md source files.")
    parser.add_argument("--instructor", help="Exports md version of question.", **_base_args)
    parser.add_argument(
        "--public", help="Exports md version of question with the answers removed.", **_base_args
    )
    parser.add_argument(
        "--prairielearn", help="Exports info.json, server.py, and question.html..", **_base_args
    )
    parser.set_defaults(func=_do_run)
    return parser


def _do_run(args: argparse.Namespace, parser: argparse.ArgumentParser):
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
            if sys.version_info >= (3, 11):
                e.add_note(f"Error in processing question: {source_filepath}")
            else:
                e.args = (f"Error in processing question: {source_filepath}", *e.args)
            excs.append(e)

    if excs:
        if sys.version_info >= (3, 11):
            raise ExceptionGroup("Errors in processing questions:", excs)
        else:
            import exceptiongroup

            raise exceptiongroup.ExceptionGroup("Errors in processing questions:", excs)

    try:
        # Copy over the html_questions directory into output/prairielearn
        html_source = source_root.parent / "html_questions"
        target = source_root.parent / "output/prairielearn/html_questions"

        shutil.copytree(html_source, target, dirs_exist_ok=True)
    except FileNotFoundError as e:
        print(e)
        print("Skipping the copying of html sources; directories not correct.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser(None)
    args = parser.parse_args(argv)
    return args.func(args, parser)


if __name__ == "__main__":
    main()
