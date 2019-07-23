#!/bin/bash

pytest --cov=app test/ --ignore=test/ignore/ -vv -s

