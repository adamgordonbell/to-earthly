#!/bin/bash

# Docker login
echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin

# Build the Docker image
docker build -t build -f build.Dockerfile .

# Run the build.sh script inside the Docker container
docker run --rm build ./build.sh

# Build the application Docker image
IMAGE_NAME="ezeev/earthly-node-example"
TAG="gh-actions-only"
docker build . --file Dockerfile --tag $IMAGE_NAME:$TAG

# Push the Docker image
docker push $IMAGE_NAME:$TAG