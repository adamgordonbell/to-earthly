#!/bin/bash
DOCKERHUB_USERNAME=<your_dockerhub_username>
DOCKERHUB_TOKEN=<your_dockerhub_token>

docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN
docker build -t ezeev/earthly-node-example:gh-actions-only -f build.Dockerfile .
docker push ezeev/earthly-node-example:gh-actions-only
