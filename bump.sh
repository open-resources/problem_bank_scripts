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
curl --silent https://raw.githubusercontent.com/PrairieLearn/PrairieLearn/refs/heads/master/apps/prairielearn/python/prairielearn/sympy_utils.py --output src/problem_bank_scripts/_vendored/sympy_utils.py
sed -i "s/from prairielearn.misc_utils import full_unidecode/from .misc_utils import full_unidecode/g" src/problem_bank_scripts/_vendored/sympy_utils.py
curl --silent https://raw.githubusercontent.com/PrairieLearn/PrairieLearn/refs/heads/master/apps/prairielearn/python/prairielearn/misc_utils.py --output src/problem_bank_scripts/_vendored/misc_utils.py
sed -i "s/from pint import UnitRegistry/UnitRegistry = None/g" src/problem_bank_scripts/_vendored/misc_utils.py
sed -i "s/from text_unidecode import unidecode/unidecode = None/g" src/problem_bank_scripts/_vendored/misc_utils.py

# commit the changes
git add pyproject.toml src/problem_bank_scripts/_vendored/sympy_utils.py src/problem_bank_scripts/_vendored/misc_utils.py
git commit -m "Increment version from $FROM to $TO"

# create a tag
git tag -a "v$TO" -m "Version $TO"

echo "Bump to version $TO complete. Remember to run 'git push' and 'git push --tags' to push the changes."
