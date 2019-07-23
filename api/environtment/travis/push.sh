#!/bin/bash
echo "$GITLAB_PASS" | docker login -u "$GITLAB_USER" --password-stdin
docker push "$GITLAB_USER"/"$REPO_NAME"