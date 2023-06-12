To recreate the steps of this GitHub Actions workflow using bash and Docker, we will create the `run.sh`, `build.Dockerfile`, and `build.sh` files.

1. Create a `run.sh` script that will be responsible for building and running the Docker container. This script will be stored in the git repository along with the code.

2. Create a `build.Dockerfile` that will define the base image and install the necessary dependencies for the build process. In this case, we will use `node:19-alpine`.

3. Create a `build.sh` script that will run the actual build steps inside the Docker container. This script will be executed within the `build.Dockerfile` image.

Now, let's go through the YAML file section by section:

- The `on` section specifies when the workflow should run. This is not relevant for our bash and Docker setup, so we can ignore it.

- The `jobs` section contains the actual build steps. We will need to adapt these steps for our `build.sh` and `build.Dockerfile` files.

  - The `actions/checkout@v3` step is not needed, as our `run.sh` and `build.sh` scripts will be stored in the git repository along with the code.

  - The `docker/login-action@v2` step should be included in the `run.sh`.

  - The `docker/build-push-action@v4` step should be included in the `run.sh`.

  - The `actions/checkout@v3` step is not needed, as our `run.sh` and `build.sh` scripts will be stored in the git repository along with the code.

  - The `actions/cache@v2` step is not needed, as Docker will handle caching for us.

  - The `actions/setup-node@v3` step is not needed, as we will use the `node:19-alpine` base image in our `build.Dockerfile`.

  - The "React Setup" and "React Service Build" steps should be included in the `build.sh`.

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

# Build and push the application Docker image
IMAGE_NAME="ezeev/earthly-react-example"
TAG="gh-actions-only"
docker build . --file Dockerfile --tag $IMAGE_NAME:$TAG
docker push $IMAGE_NAME:$TAG
```

`build.Dockerfile`:

```
# Use a Node.js 19 alpine base image
FROM node:19-alpine

# Set the working directory
WORKDIR /app

# Copy the build.sh script into the image
COPY build.sh ./

# Install global dependencies
RUN npm install -g typescript
```

`build.sh`:

```bash
#!/bin/bash

# Install local dependencies
npm install

# Run the React Service Build
VITE_RUST_SERVER=http://localhost:8000 \
VITE_GO_SERVER=http://localhost:8001 \
VITE_PYTHON_SERVER=http://localhost:8002 \
VITE_NODE_SERVER=http://localhost:8003 \
npm run build
```