#!/bin/bash

# Clone the repository (assuming it's not already cloned)
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository

# Log in to Docker Hub
echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin

# Build the Docker image
docker build -t ezeev/earthly-react-example:gh-actions-only -f build.Dockerfile .

# Push the Docker image
docker push ezeev/earthly-react-example:gh-actions-only

# Run the build process inside the Docker container
docker run --rm ezeev/earthly-react-example:gh-actions-only
