# This file is based off of https://github.com/pre-commit/pre-commit-hooks/blob/main/pre_commit_hooks/check_ast.py
from __future__ import annotations

import argparse
import ast
import platform
import traceback
from collections.abc import Sequence
from pathlib import Path

from problem_bank_scripts import assemble_server_py, read_md_problem


def create_parser(subparsers: argparse._SubParsersAction | None) -> argparse.ArgumentParser:
    if subparsers is None:
        parser = argparse.ArgumentParser()
    else:
        parser = subparsers.add_parser(
            "check-server-ast",
            description="Check server code ast for one or more markdown files.",
            help="Check server code ast for one or more markdown files.",
        )
    parser.add_argument("filenames", nargs="*")
    parser.set_defaults(func=_do_run)
    return parser


def _do_run(args: argparse.Namespace, parser: argparse.ArgumentParser):
    impl = platform.python_implementation()
    version = platform.python_version()

    retval = 0
    for filename in args.filenames:
        if "source" not in filename or "README.md" in filename:
            continue
        file = read_md_problem(filename)
        code = assemble_server_py(file, "local")
        try:
            ast.parse(code, filename=f"<{Path(filename).stem}:server.py>", type_comments=True)
        except SyntaxError:
            print(f"{filename}: failed parsing with {impl} {version}:")
            tb = "    " + traceback.format_exc().replace("\n", "\n    ")
            print(f"\n{tb}")
            retval = 1
    return retval


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser(None)
    args = parser.parse_args(argv)
    return args.func(args, parser)


if __name__ == "__main__":
    raise SystemExit(main())
