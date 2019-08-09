.PHONY: all clean build

all: build upload clean

test:
			pytest --cov=neo --cov-report=term-missing

build:
			rm -rf dist
			python setup.py sdist
			gpg --detach-sign -a dist/*

docker_build: 
			docker build .

devel: 
			pip3 install -e .

upload:
			twine upload dist/*

clean:
			find . -d -name "__pycache__" -exec rm -rf {} \;
			rm -rf .coverage temp neo_cli.egg-info dist build .pytest_cache .ropeproject
