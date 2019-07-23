#!/bin/bash
docker login -u "$GITLAB_USER_MY" -p "$GITLAB_PASS_MY" registry.gitlab.com
docker build -t registry.gitlab.com/riszkymf/restknot:$TRAVIS_TAG .
docker push registry.gitlab.com/riszkymf/restknot:$TRAVIS_TAG