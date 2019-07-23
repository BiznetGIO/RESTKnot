#!/bin/bash
chmod +x run_travis.sh
./run_travis.sh
pytest --cov=app test/ --ignore=test/ignore/ -vv -s
