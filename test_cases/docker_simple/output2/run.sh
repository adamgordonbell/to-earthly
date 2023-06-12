#!/bin/bash

# Build the Docker image
IMAGE_NAME="my-image-name"
TAG=$(date +%s)

# Build the application Docker image
docker build . --file Dockerfile --tag $IMAGE_NAME:$TAG