#!/bin/zsh

echo "Checking" $1
ruff check $1
isort --check $1 # remove when https://github.com/astral-sh/ruff/issues/8232 is resolved
mypy --check-untyped-defs $1
