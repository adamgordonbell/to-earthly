To recreate the steps of this GitHub Actions workflow using bash and Docker, we will create the following files:

1. `run.sh`: A bash script that wraps Docker commands and runs the build process.
2. `build.Dockerfile`: A Dockerfile that sets up the base image, installs dependencies, and copies necessary files.
3. `build.sh`: A bash script that runs the build steps inside the Docker container.

Here's how we would approach each section of the GitHub Actions workflow:

- `on` section: This section defines the events that trigger the workflow. We don't need to include this in our bash and Docker setup, as it's specific to GitHub Actions.

- `jobs` section: This section defines the jobs that run in the workflow. We will recreate these steps in our `run.sh` and `build.sh` scripts.

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
docker run --rm -v "$(pwd)":/app -w /app ezeev/earthly-react-example:gh-actions-only ./build.sh
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

In summary, we have created a `run.sh` script that handles cloning the repository, logging in to Docker Hub, building and pushing the Docker image, and running the build process inside the Docker container. The `build.Dockerfile` sets up the base image, installs dependencies, and copies necessary files. Finally, the `build.sh` script runs the build steps inside the Docker container.