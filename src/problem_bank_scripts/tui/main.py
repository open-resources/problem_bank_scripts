import argparse
import os
import pathlib
import shutil

import nltk
from dotenv import load_dotenv

from .tui import run_tui


REQUIRED_ENV_VARS = ["GITHUB_USERNAME", "WRITE_PATH", "PL_QUESTION_PATH", "MY_NAME", "MY_INITIALS"]
_REQ_VARS_TEXT = (
    ", ".join(f"{var!r}" for var in REQUIRED_ENV_VARS[:-1]) + f", and {REQUIRED_ENV_VARS[-1]!r}"
)


class _Formatter(argparse.HelpFormatter):
    def __init__(self, prog: str) -> None:
        width = shutil.get_terminal_size().columns
        super().__init__(prog, max_help_position=32, width=min(120, width - 2))


_description = (
    "Create a barebones OPB markdown question via a series of tui prompts. "
    "It requires the following environment variables to be set, either via '--env-file', "
    f"or in the shell's environment: {_REQ_VARS_TEXT}"
)
_epilog = (
    "This program requires both 'git' and 'gh' to be installed to create PRs. "
    "You can find the installation instructions for 'gh' at https://github.com/cli/cli#installation."
)


def create_parser(subparsers: argparse._SubParsersAction | None) -> argparse.ArgumentParser:
    if subparsers is None:
        parser = argparse.ArgumentParser(
            formatter_class=_Formatter,
            description=_description,
            epilog=_epilog,
        )
    else:
        parser = subparsers.add_parser(
            "create-question",
            formatter_class=_Formatter,
            description=_description,
            epilog=_epilog,
            help="Create a barebones OPB markdown question via a series of tui prompts.",
        )
    parser.add_argument(
        "--create-pr",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Create a PR with the generated question.",
    )
    parser.add_argument(
        "--gpt",
        action="store_true",
        help=(
            "Use ChatGPT gpt-4o-mini to generate the MCQ options and number input code. "
            "If this is specified, the environment variable 'OPENAI_API_KEY' is also required "
            "to be available, or be in the env file specified by --env-file. (default: %(default)s)"
        ),
    )
    parser.add_argument(
        "--saved-json",
        action="store",
        default="./saved.json",
        help="File to read/save tui prompts to/from. (default: %(default)s)",
    )
    env_file = parser.add_mutually_exclusive_group()
    env_file.add_argument(
        "--env-file",
        action="store",
        default=".env",
        help="Path to the environment file with the required environment variables (default: %(default)s)",
    )
    env_file.add_argument(
        "--no-env-file",
        action="store_false",
        help=(
            "Do not read from any environment file. "
            "If you use this, make sure the required environment variables are set in your shell's environment.  (default: False)"
        ),
    )
    parser.set_defaults(func=_do_run)
    return parser


def _do_run(args: argparse.Namespace, parser: argparse.ArgumentParser):
    CREATE_PR = args.create_pr
    USE_GPT = args.gpt

    if args.no_env_file:
        ENV_FILE = pathlib.Path(args.env_file).expanduser().resolve()
        print(f"Loading environment variables from '{ENV_FILE}'.")
        load_dotenv(ENV_FILE)

    if USE_GPT and "OPENAI_API_KEY" not in os.environ:
        parser.error(
            "The 'OPENAI_API_KEY' environment variable is required when using the --gpt flag."
        )

    if CREATE_PR and shutil.which("gh") is None:
        parser.error(
            "The 'gh' command is required to create a PR. "
            "Please install it following the instructions at https://github.com/cli/cli#installation"
        )

    if CREATE_PR and shutil.which("git") is None:
        parser.error("The 'git' command is required to create a PR. Please install it.")

    for var in REQUIRED_ENV_VARS:
        if var not in os.environ:
            parser.error(
                f"The environment variable {var!r} is required."
                "Please set it in your shell's environment or in the specified environment file."
            )

    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)

    return run_tui(create_pr=CREATE_PR, use_gpt=USE_GPT) or 0


def main():  # ruff: #noqa: ANN201
    parser = create_parser(None)
    args = parser.parse_args()
    return args.func(args, parser)
