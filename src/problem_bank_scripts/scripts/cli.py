# Top level script for running various scripts in PBS via subcommands.

import argparse
from collections.abc import Sequence

from .check_question import create_parser as checkq_parser
from .check_server_ast import create_parser as check_server_ast_parser
from .lint_server import create_parser as lint_server_parser
from .process import create_parser as process_parser
from .process_q import create_parser as process_q_parser


try:
    # the tui requires optional dependencies, so we only import it if it is available
    from problem_bank_scripts.tui.main import create_parser as tui_parser
except ImportError:
    tui_parser = None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="OPB Problem Bank Scripts CLI",
    )
    subparsers = parser.add_subparsers()
    checkq_parser(subparsers)
    check_server_ast_parser(subparsers)
    lint_server_parser(subparsers)
    process_q_parser(subparsers)
    process_parser(subparsers)
    if tui_parser is not None:
        tui_parser(subparsers)
    args = parser.parse_args(argv)
    return args.func(args, parser) or 0


if __name__ == "__main__":
    raise SystemExit(main())
