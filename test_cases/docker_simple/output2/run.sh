#!/bin/bash

# Build the Docker image
IMAGE_NAME="my-image-name"
TAG=$(date +%s)
docker build . --file build.Dockerfile --tag $IMAGE_NAME:$TAG

# Run the build.sh script inside the Docker container
docker run --rm $IMAGE_NAME:$TAG ./build.sh

# Build the application Docker image
docker build . --file Dockerfile --tag $IMAGE_NAME:$TAG

# Push the Docker image to a container registry (optional)
# docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
# docker push $IMAGE_NAME:$TAG
