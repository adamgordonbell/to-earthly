Here are the `run.sh`, `build.Dockerfile`, and `build.sh` files:

`run.sh`:
```bash
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
```

`build.Dockerfile`:
```Dockerfile
FROM node:19

WORKDIR /app

COPY package*.json ./

RUN npm install -g typescript
RUN npm ci

COPY . .

CMD ["./build.sh"]
```

`build.sh`:
```bash
#!/bin/bash

# Set environment variables
export VITE_RUST_SERVER=http://localhost:8000
export VITE_GO_SERVER=http://localhost:8001
export VITE_PYTHON_SERVER=http://localhost:8002
export VITE_NODE_SERVER=http://localhost:8003

# Run the React build process
npm run build
```

In this version, we have removed the volume mounting from the `run.sh` script, and the `build.Dockerfile` now copies all necessary files into the Docker image. The `build.sh` script remains the same, running the build steps inside the Docker container.