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

# change any references to the old version in the project
echo "Bumping version from $FROM to $TO in src/problem_bank_scripts/__init__.py"
sed -i "s/__version__ = \"$FROM\"/__version__ = \"$TO\"/g" src/problem_bank_scripts/__init__.py
echo "Bumping version from $FROM to $TO in tests/test_problem_bank_scripts.py"
sed -i "s/__version__ == \"$FROM\"/__version__ == \"$TO\"/g" tests/test_problem_bank_scripts.py

# commit the changes
git add src/problem_bank_scripts/__init__.py tests/test_problem_bank_scripts.py pyproject.toml
git commit -m "Increment version from $FROM to $TO"

# create a tag
git tag -a "v$TO" -m "Version $TO"

echo "Bump to version $TO complete. Remember to run 'git push --tags' to push the changes."
