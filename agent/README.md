# RESTKnot Agent

## Installation

You can run the it locally or using Docker container with specied Dockerfile.

Locally:

``` python
pip install -r requirements.txt
pip install -e .

# run the app: dnsagent start [master | slave]
dnsagent start master
```

Using docker:

``` python
# build the image
docker build -f Dockerfile -t restknot-agent:0.7.0 .

# run via docker-compose
docker-compose -f docker-compose.yml up
```
