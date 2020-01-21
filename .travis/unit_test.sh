#!/bin/bash
pip install -r api/requirements.txt
pip install -r api/requirements-dev.txt

pytest -vv -s api/tests/unit/
