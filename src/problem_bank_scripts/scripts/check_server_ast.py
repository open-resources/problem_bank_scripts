# This file is based off of https://github.com/pre-commit/pre-commit-hooks/blob/main/pre_commit_hooks/check_ast.py
from __future__ import annotations

import argparse
import ast
import platform
import sys
import traceback
from typing import Sequence
from pathlib import Path

from ..problem_bank_scripts import read_md_problem, assemble_server_py

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        if "source" not in filename or "README.md" in filename:
            continue
        file = read_md_problem(filename)
        code = assemble_server_py(file, "local")
        try:
            ast.parse(code, filename=f"<{Path(filename).stem}:server.py>", type_comments=True)
        except SyntaxError:
            impl = platform.python_implementation()
            version = sys.version.split()[0]
            print(f'{filename}: failed parsing with {impl} {version}:')
            tb = '    ' + traceback.format_exc().replace('\n', '\n    ')
            print(f'\n{tb}')
            retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())