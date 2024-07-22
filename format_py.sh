#!/bin/zsh

echo "Formatting " $1
ruff check --fix $1  # remove when https://github.com/astral-sh/ruff/issues/8232 is resolved
ruff format $1
