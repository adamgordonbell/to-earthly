#!/bin/bash

# Docker login
echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin

# Build the Docker image
docker build -t build -f build.Dockerfile .

# Run the build.sh script inside the Docker container
docker run --rm -v $(pwd):/app build ./build.sh

# Build and push the application Docker image
IMAGE_NAME="ezeev/earthly-react-example"
TAG="gh-actions-only"
docker build . --file Dockerfile --tag $IMAGE_NAME:$TAG
docker push $IMAGE_NAME:$TAG