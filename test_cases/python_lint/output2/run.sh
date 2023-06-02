#!/bin/bash

# Build the Docker image
docker build -t python-build -f build.Dockerfile .

# Run the build.sh script inside the Docker container
docker run --rm python-build ./build.sh
