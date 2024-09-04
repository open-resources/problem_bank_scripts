# Problem Bank Scripts 

[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/problem-bank-scripts.svg)](https://pypi.org/project/problem-bank-scripts/)
[![PyPI version info](https://img.shields.io/pypi/v/problem-bank-scripts.svg)](https://pypi.org/project/problem-bank-scripts/)
[![codecov](https://codecov.io/gh/open-resources/problem_bank_scripts/branch/main/graph/badge.svg)](https://codecov.io/gh/open-resources/problem_bank_scripts)
[![Documentation Status](https://readthedocs.org/projects/problem_bank_scripts/badge/?version=latest)](https://problem-bank-scripts.readthedocs.io/en/latest/?badge=latest)


## Installation

```bash
pip install problem_bank_scripts
```

## Update version

Here are the steps to increment the version (replace patch with major/minor/patch):

First, make sure to have the latest changes in the main branch.

```bash
git checkout main && git pull
```

Then, make sure all tests pass before incrementing the version.

```bash
poetry run pytest
```

Finally, increment the version and push the new tag and version change.

```bash
bash bump.sh patch

git push && git push --tags
```

To finalize the version update, create a new release on GitHub and the package will be automatically published
 to PyPI after the deployment is approved assuming all tests pass.

## Features

- TODO

## Dependencies

- TODO

## Usage

- TODO

## Documentation

The official documentation is hosted on Read the Docs: https://problem-bank-scripts.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/open-resources/problem_bank_scripts/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
