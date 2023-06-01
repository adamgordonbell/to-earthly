#!/bin/bash

# Log in to Docker Hub
DOCKERHUB_USERNAME=<your_dockerhub_username>
DOCKERHUB_TOKEN=<your_dockerhub_token>
docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN

# Build the build image
docker build -t build-image -f build.Dockerfile .

# Run the build script inside the build container
docker run --name build-container build-image ./build.sh

# Copy the built files from the build container to the host
docker cp build-container:/app/dist ./dist

# Remove the build container
docker rm build-container

# Build the application image
docker build -t ezeev/earthly-node-example:gh-actions-only .

# Push the application image
docker push ezeev/earthly-node-example:gh-actions-only
