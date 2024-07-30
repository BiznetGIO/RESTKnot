#!/usr/bin/env -S just --justfile

alias f := fmt
alias l := lint
alias c := comply
alias k := check

# List available commands.
_default:
    just --list --unsorted

# Tasks to make the code-base comply with the rules. Mostly used in git hooks.
comply: fmt lint

# Check if the repository comply with the rules and ready to be pushed.
check: fmt-check lint

# Format the codebase.
fmt:
    dprint fmt

# Check is the codebase properly formatted.
fmt-check:
    dprint check

# Lint the codebase.
lint:
    # Run `typos  --write-changes` to fix the mistakes
    typos
