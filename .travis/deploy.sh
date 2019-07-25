#!/bin/bash
cd api
docker login -u "$GITLAB_USER" -p "$GITLAB_PASS" registry.gitlab.com
docker build -t "$URL_REGISTRY_API":"$TRAVIS_TAG" .
docker push "$URL_REGISTRY_API":"$TRAVIS_TAG"
cd ../agent
docker login -u "$GITLAB_USER" -p "$GITLAB_PASS" registry.gitlab.com
docker build -t "$URL_REGISTRY_AGENT":"$TRAVIS_TAG" .
docker push "$URL_REGISTRY_AGENT":"$TRAVIS_TAG"