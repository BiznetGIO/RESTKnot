#!/bin/bash
cd api
docker login -u "$SECRET_MY_GITLAB_USER=" -p "$SECRET_MY_GITLAB_PASS=" registry.gitlab.com
docker build -t "$URL_REGISTRY":"$TRAVIS_TAG" .
docker push "$URL_REGISTRY":"$TRAVIS_TAG"
cd ../agent
docker login -u "$SECRET_MY_GITLAB_USER" -p "$SECRET_MY_GITLAB_PASS" registry.gitlab.com
docker build -t "$URL_REGISTRY":"$TRAVIS_TAG" .
docker push "$URL_REGISTRY":"$TRAVIS_TAG"