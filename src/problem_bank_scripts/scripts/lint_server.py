# This file is based off of https://github.com/pre-commit/pre-commit-hooks/blob/main/pre_commit_hooks/check_ast.py
from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
from textwrap import indent

from black import format_str
from black.mode import Mode, TargetVersion

from problem_bank_scripts import read_md_problem


def create_parser(subparsers: argparse._SubParsersAction | None) -> argparse.ArgumentParser:
    if subparsers is None:
        parser = argparse.ArgumentParser()
    else:
        parser = subparsers.add_parser(
            "lint-server",
            description="Lint the server code ast for one or more markdown files.",
            help="Lint the server code ast for one or more markdown files.",
        )
    parser.add_argument("filenames", nargs="*")
    parser.set_defaults(func=_do_run)
    return parser


def _do_run(args: argparse.Namespace, parser: argparse.ArgumentParser):
    """Pre-Commit hook to lint server.py sections in OPB problems

    Args:
        argv (Sequence[str], optional): Arguments passed to the script. Defaults to None.

    Returns:
        code: A return code of 0 indicates success, 1 indicates failure, similar to bash return codes.
    """
    retval = 0
    for filename in args.filenames:
        if "source" not in filename or "README.md" in filename:
            continue
        try:
            file = read_md_problem(filename)
        except:
            retval = 1
            print(f"Error reading {filename}")
            continue
        try:
            server_dict = file["header"].get("server", {})
        except:
            retval = 1
            print(f"Error reading yaml header from {filename}")
            continue
        reformatted_sections = []
        try:
            for section, code in server_dict.items():
                formatted = format_str(
                    code,
                    mode=Mode(target_versions={TargetVersion.PY310}, line_length=100),
                )
                if formatted != code:
                    reformatted_sections.append(section)
                server_dict[section] = formatted
            if reformatted_sections:
                retval = 1
                print(f"Reformatted sections of {filename}: {reformatted_sections}")
                file["header"]["server"] = server_dict
                server_yml = ""
                for section, code in server_dict.items():
                    server_yml += f"{section}: |\n{indent(code, '    ')}\n"
                path = Path(filename)
                contents = path.read_text()
                pre_server, server, post_server = contents.partition("server:\n")
                _, part1, remaining = post_server.partition("part1:\n")
                path.write_text(
                    f"{pre_server}{server}{indent(server_yml, '    ')}{part1}{remaining}"
                )
        except:
            retval = 1
            print(f"Error formatting {filename}")
            continue

    return retval


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser(None)
    args = parser.parse_args(argv)
    return args.func(args, parser)


if __name__ == "__main__":
    raise SystemExit(main())
