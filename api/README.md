# RESTKnot API

## Installation

You can run the it via `flask run` or using Docker with specied Dockerfile.

``` python
# install the requirements

pip3 install -r requirements.txt
flask run
```

Using docker:

``` python
# build the image
docker build -f Dockerfile -t restknot-api:0.7.0 .

# run via docker-compose
docker-compose -f docker-compose.yml up
```

