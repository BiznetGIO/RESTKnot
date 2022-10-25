#!/usr/bin/env -S just --justfile

shebang := if os() == 'windows' { 'powershell.exe' } else { '/usr/bin/sh' }

set dotenv-load := true

# List available commands.
_default:
    just --list --unsorted

# Setup the repository.
setup:
    python  -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python -m pip install -r api/requirements.txt
    python -m pip install -r api/requirements-dev.txt
    python -m pip install -r agent/requirements.txt

# Setup the repository.
clean:
    #!{{ shebang }}
    rm -rf .venv

# Develop the app.
dev app="api":
    #!{{ shebang }}
    if [ "{{ app }}" = "api" ]; then
        just api/dev
    fi

# Format the codebase.
fmt:
    black api agent
    isort --settings-path api/setup.cfg api
    isort --settings-path agent/setup.cfg agent

# Check is the codebase properly formatted.
fmt-check:
    black --check api agent

# Lint the codebase.
lint:
    flake8 --config api/setup.cfg api
    flake8 --config agent/setup.cfg agent

_test-unit:
    pytest -s api/tests/unit/

# Test the codebase.
test: _test-unit
    pytest -s api/tests/integration/

# Tasks to make the code-base comply with the rules. Mostly used in git hooks.
comply: fmt lint test

# Check if the repository comply with the rules and ready to be pushed.
check: fmt-check lint test
