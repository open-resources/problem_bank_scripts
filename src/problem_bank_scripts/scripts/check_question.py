# Author: Firas Moosvi
# Date: 2023-05-14

import argparse
import pathlib
import sys

from problem_bank_scripts import process_question_pl


def main():
    parser = argparse.ArgumentParser(
        description="Syntax check on an individual question.",
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
    args = parser.parse_args()
    output_root: pathlib.Path = args.output_root 
    question: pathlib.Path = args.md_file

    if question.suffix.lower() != ".md":
        parser.error(f"You must provide a path to an .md file - '{question}' is not an md file!")

    output_dir = output_root.joinpath(*question.parts[-2:])

    # Process md file
    try:
        print(f"Processing question: {question}")

        process_question_pl(question.as_posix(), output_path=output_dir)

        print(f"\t Moved file to location: {output_dir.parent}")

    except FileNotFoundError:
        print(f"This question's file was not found. \n\tSkipping question: {question}.")
        sys.exit(2)

    except Exception as e:
        print(f"There is an error in this problem: \n\t- File path: {question}\n\t- Error: {e}")
        raise


if __name__ == "__main__":
    main()
