`run.sh`:

```bash
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

# Copy the necessary files into the container
cp -r /app .

# Install local dependencies
npm install

# Run the React Service Build
VITE_RUST_SERVER=http://localhost:8000 \
VITE_GO_SERVER=http://localhost:8001 \
VITE_PYTHON_SERVER=http://localhost:8002 \
VITE_NODE_SERVER=http://localhost:8003 \
npm run build
```

In this version, we have updated the `run.sh` script to include a volume mount for the current working directory to the `/app` directory inside the container. This allows the `build.sh` script to access the necessary files without needing to copy them into the `build.Dockerfile`.