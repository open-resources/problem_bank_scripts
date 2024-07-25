# Author: Firas Moosvi
# Date: 2023-05-14

import argparse
import pathlib
from collections.abc import Sequence

from problem_bank_scripts import process_question_pl

from . import check_server_ast


def create_parser(subparsers: argparse._SubParsersAction | None) -> argparse.ArgumentParser:
    if subparsers is None:
        parser = argparse.ArgumentParser(
            description="Syntax check on an individual question.",
            allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    else:
        parser = subparsers.add_parser(
            "checkq",
            description="Syntax check on an individual question.",
            allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            help="Check the syntax of a single question.",
        )
    parser.add_argument(
        "md_file",
        type=pathlib.Path,
        action="store",
        help="Path to the source md file.",
    )
    parser.add_argument(
        "--output_root",
        type=pathlib.Path,
        default="../pl-opb-ind100/questions",
        help="Location where the question folder should export.",
        metavar="<str>",
    )
    parser.set_defaults(func=_do_run)
    return parser


def _do_run(args: argparse.Namespace, parser: argparse.ArgumentParser):
    output_root: pathlib.Path = args.output_root
    question: pathlib.Path = args.md_file

    if question.suffix.lower() != ".md":
        parser.error(f"You must provide a path to an .md file - '{question}' is not an md file!")

    output_dir = output_root.joinpath(*question.parts[-2:])

    # Process md file
    try:
        print(f"Processing question: {question}")

        if check_server_ast.main([question.as_posix()]) != 0:
            return -1

        process_question_pl(question.as_posix(), output_path=output_dir)

        print(f"\t Moved file to location: {output_dir.parent}")

    except FileNotFoundError:
        print(f"This question's file was not found. \n\tSkipping question: {question}.")

    except Exception as e:
        print(f"There is an error in this problem: \n\t- File path: {question}\n\t- Error: {e}")
        return -1


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser(None)
    args = parser.parse_args(argv)
    return args.func(args, parser)


if __name__ == "__main__":
    raise SystemExit(main())
