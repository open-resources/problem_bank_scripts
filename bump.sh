#!/bin/bash

VERSION_LEVEL=$1

if [ -z "$VERSION_LEVEL" ]; then
    echo "Usage: $0 <VERSION_LEVEL>"
    echo "  VERSION_LEVEL: The level of the version to bump. One of: patch, minor, major"
    exit 1
fi

# Bump the version and save poetry output to string
ret=$(poetry version $VERSION_LEVEL)
echo $ret
FROM=$(echo $ret | awk '{ print $4; }')
TO=$(echo $ret | awk '{ print $6; }')

# Update "vendored" copy of PrairieLearn's python utilities
curl --silent https://raw.githubusercontent.com/PrairieLearn/PrairieLearn/master/apps/prairielearn/python/python_helper_sympy.py --output src/problem_bank_scripts/_vendored/python_helper_sympy.py
sed -i "s/import prairielearn as pl/from . import prairielearn as pl/g" src/problem_bank_scripts/_vendored/python_helper_sympy.py

# commit the changes
git add src/problem_bank_scripts/__init__.py tests/test_problem_bank_scripts.py pyproject.toml src/problem_bank_scripts/_vendored/python_helper_sympy.py
git commit -m "Increment version from $FROM to $TO"

# create a tag
git tag -a "v$TO" -m "Version $TO"

echo "Bump to version $TO complete. Remember to run 'git push' and 'git push --tags' to push the changes."
