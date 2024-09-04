# Author: Firas Moosvi
# Date: 2022-07-09

import argparse
import os
import pathlib
from collections.abc import Sequence

import git

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


_base_args = {"type": _bool, "action": "store", "default": True, "metavar": "<bool>"}

_usage = """
  %(prog)s [--instructor <bool>] [--public <bool>] [--prairielearn <bool>] [--temp_output_root <str>] md_file
  %(prog)s [--instructor <bool>] [--public <bool>] [--prairielearn <bool>] [--temp_output_root <str>] [--pullrequest <bool>]\
"""


def create_parser(subparsers: argparse._SubParsersAction | None) -> argparse.ArgumentParser:
    if subparsers is None:
        parser = argparse.ArgumentParser(
            description="Syntax check on an individual question.",
            allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            usage=_usage,
        )
    else:
        parser = subparsers.add_parser(
            "process-q",
            description="Syntax check on an individual question.",
            allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            usage=_usage,
            help="Check the syntax of a single question.",
        )
    parser.add_argument("md_file", action="store", help="Path to the source md file.", nargs="?")
    parser.add_argument("--instructor", help="Exports md version of question.", **_base_args)
    parser.add_argument(
        "--public", help="Exports md version of question with the answers removed.", **_base_args
    )
    parser.add_argument(
        "--prairielearn", help="Exports info.json, server.py, and question.html..", **_base_args
    )
    parser.add_argument(
        "--temp_output_root",
        help="Temporary output path this directory should be in gitignore",
        default="tmp_output",
        metavar="<str>",
    )
    parser.add_argument(
        "--pullrequest",
        help="Flag to scan the current branch for any .md files different from the main branch",
        type=_bool,
        action="store",
        default=False,
    )
    parser.set_defaults(func=_do_run)
    return parser


def _do_run(args: argparse.Namespace, parser: argparse.ArgumentParser):
    questions: list[str] = []

    temp_output_root = args.temp_output_root

    if args.pullrequest and args.md_file:
        parser.print_usage()
        parser.exit(2)

    if args.pullrequest:
        repo = git.Repo("./")
        questions.extend(
            repo.git.diff("origin/main", "--name-only", "source/**/*.md")
            .replace("\n", ";")
            .split(";")
        )
        pull_req = True
    else:
        questions.append(args.md_file)
        pull_req = False

    formatted_q_list = "\n-".join(questions)
    print(f"The following questions have changed in this PR compared to main: { formatted_q_list }")

    if pathlib.Path(questions[0]).suffix.lower() != ".md":
        parser.error(
            "You should check the location of your changed md files, it seems no markdown files were changed in the `source` directory!"
        )

    # Process md files
    for md_file in questions:
        try:
            print(f"Processing file: {md_file}")
            if args.instructor:
                temp_output_path = pathlib.Path(
                    md_file.replace("source", os.path.join(temp_output_root, "instructor"))
                )
                process_question_md(md_file, instructor=True, output_path=temp_output_path)

            if args.public:
                temp_output_path = pathlib.Path(
                    md_file.replace("source", os.path.join(temp_output_root, "public"))
                )
                process_question_md(md_file, instructor=False, output_path=temp_output_path)

            if args.prairielearn:
                temp_output_path = pathlib.Path(
                    md_file.replace("source", os.path.join(temp_output_root, "prairielearn"))
                )
                process_question_pl(md_file, output_path=temp_output_path, dev=pull_req)

            print(f"\t Completed file: {md_file} in location: {temp_output_root}")

        except FileNotFoundError as fne:
            # print(f"There are new questions merged into main that are not present in this branch. \n\tSkipping question: {md_file}.")
            print(f"Skipping question: {md_file}:")
            print(
                "\tThere are either new questions merged into main that are not present in this branch, or an expected asset is missing:"
            )
            print(f"\t\tNo such file or directory: {fne.filename}")
            continue

        except Exception as e:
            print(f"There is an error in this problem: \n\t- File path: {md_file}\n\t- Error: {e}")
            raise


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser(None)
    args = parser.parse_args(argv)
    return args.func(args, parser)


if __name__ == "__main__":
    raise SystemExit(main())
