.PHONY: help clean setup sort sort_check fmt fmt_check lint lint_check comply check
.DEFAULT_GOAL := help

help: # https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	rm -fr build dist .egg requests.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.log' -delete

setup: ## Setup the repository.
	# activate your venv before running this command
	pip install -r api/requirements.txt
	pip install -r api/requirements-dev.txt
	pip install -r agent/requirements.txt

	pip install black==21.12b0 pylint==2.12.2 mypy==0.930 isort==5.10.1
	pip install types-PyYAML

	# add `make comply` to your `.git/hooks/pre-commit`

sort: ## Sort the imports inside codebase.
	isort .

sort_check: ## Check is the codebase imopors is sorted.
	isort --check-only .

fmt: ## Format the codebase.
	black .

fmt_check: ## Check is the codebase properly formatted.
	black --check .

lint: ## Lint the codebase.

	# `pylint .` can't work without `__init__.py` file
	pylint api
	pylint agent

	mypy .

test_unit:
	pytest --capture=no --verbose api/tests/unit/

test: test_unit
	pytest --capture=no --verbose api/tests/integration/

comply: sort fmt lint test_unit ## Tasks to make the code-base comply with the rules. Mostly used in git hooks.

check: sort_check fmt_check lint test ## Check if the repository comply with the rules and ready to be pushed.
