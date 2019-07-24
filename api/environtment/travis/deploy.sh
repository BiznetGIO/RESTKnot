#!/bin/bash
docker login -u "$GITLAB_USER_MY" -p "$GITLAB_PASS_MY" registry.gitlab.com
docker build -t $TRAVIS_TAG registry.gitlab.com/riszkymf/restknot .
docker push registry.gitlab.com/riszkymf/restknot