#!/bin/zsh

echo "Formatting " $1
black $1
isort $1