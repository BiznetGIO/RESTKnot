.DEFAULT_GOAL := help

help: # https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Setup the repository.
	echo "::: Setting up..."
	python -m pip install -r requirements.txt

fmt: ## Format the codebase.
	black .

	isort --settings-path setup.cfg .

fmt_check: ## Check is the codebase properly formatted.
	black --check .

lint: ## Lint the codebase.
	flake8 --config setup.cfg .

comply: fmt lint ## Tasks to make the code-base comply with the rules. Mostly used in git hooks.

check:  fmt_check lint ## Check if the repository comply with the rules and ready to be pushed.
