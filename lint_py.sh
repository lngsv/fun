#!/bin/zsh

echo "Checking" $1
ruff check $1
mypy --check-untyped-defs $1
