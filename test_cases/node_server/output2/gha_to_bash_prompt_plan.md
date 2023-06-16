To recreate the steps of this GitHub Actions workflow using bash and Docker, we will modify the `run.sh` script to build the Docker image, push it to a container registry, and run the Node.js build and test steps. We will also need to create the `build.Dockerfile` and the `build.sh` script.

1. Create a `run.sh` script that will be responsible for building and running the Docker container. This script will be stored in the git repository along with the code.

2. Create a `build.Dockerfile` that will define the base image and install the necessary dependencies for the build process. In this case, we will use `node:19` as the base image.

3. Create a `build.sh` script that will run the actual build steps inside the Docker container. This script will be executed within the `build.Dockerfile` image.

Now, let's go through the YAML file section by section:

- The `on` section specifies when the workflow should run. This is not relevant for our bash and Docker setup, so we can ignore it.

- The `jobs` section contains the actual build steps. We will need to adapt these steps for our `build.sh` and `build.Dockerfile` files.

  - The `actions/checkout@v3` step is not needed, as our `run.sh` and `build.sh` scripts will be stored in the git repository along with the code.

  - The `docker/login-action@v2` step should be included in the `run.sh`.

  - The `docker/build-push-action@v4` step should be included in the `run.sh`.

  - The `actions/checkout@v3` step is not needed, as our `run.sh` and `build.sh` scripts will be stored in the git repository along with the code.

  - The `actions/cache@v2` step is not needed, as Docker will handle caching for us.

  - The `actions/setup-node@v3` step is not needed, as we will use a Node.js base image in our `build.Dockerfile`.

  - The "Node Service Build" and "Node Service Test" steps should be included in the `build.sh`.

Here are the files:

`run.sh`:

```bash
#!/bin/bash

# Docker login
echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin

# Build the Docker image
docker build -t build -f build.Dockerfile .

# Run the build.sh script inside the Docker container
docker run --rm build ./build.sh

# Push the Docker image
IMAGE_NAME="ezeev/earthly-node-example"
TAG="gh-actions-only"
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