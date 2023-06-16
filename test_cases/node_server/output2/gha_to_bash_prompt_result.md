`run.sh`:

```bash
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
```

`build.Dockerfile`:

```
# Use a Node.js base image
FROM node:19

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the source code
COPY . .

# Copy the build.sh script into the image
COPY build.sh ./
```

`build.sh`:

```bash
#!/bin/bash

# Run the Node.js build
npm install

# Run the Node.js tests
npm test
```