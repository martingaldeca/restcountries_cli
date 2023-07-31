#!make
SHELL := /bin/bash
MAKEFLAGS += --no-print-directory

# Install dependencies
poetry-test:
	poetry install --with test
poetry-autohooks:
	poetry install --with autohooks
poetry-local:
	poetry install --with local
poetry-docs:
	poetry install --with docs
poetry-lint:
	poetry install --with lint
poetry-formatting:
	poetry install --with formatting
poetry-all: poetry-test poetry-autohooks poetry-local poetry-docs poetry-lint poetry-formatting

# Formatting
black:
	black .
isort:
	isort .
code-style: isort black

# Code quality validation
ruff:
	ruff check .
pylint:
	pylint --fail-under=8 restcountries_cli
mypy:
	mypy restcountries_cli
linters: ruff pylint mypy

# Local dev
ipython:
	ipython --InteractiveShellApp.exec_lines "['%autoreload 2', 'from restcountries_cli.factories import *', 'from restcountries_cli.cli import *']" --InteractiveShellApp.extensions autoreload
autohooks:
	poetry run autohooks activate --mode poetry

# Testing
test:
	pytest -n auto --cov=restcountries_cli --cov-report html
