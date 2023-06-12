To recreate the steps of this GitHub Actions workflow using bash and Docker, we will modify the `run.sh` script to build the Docker image. We will also need to create the `build.Dockerfile` and the `build.sh` script.

1. Create a `run.sh` script that will be responsible for building the Docker image. This script will be stored in the git repository along with the code.

2. Create a `build.Dockerfile` that will define the base image and install the necessary dependencies for the build process. In this case, we have no steps to run in the build, so we can use `alpine:latest`.

3. Create a `build.sh` script that will run the actual build steps inside the Docker container. This script will be executed within the `build.Dockerfile` image. In this case, there are no steps in the workflow besides building a dockerfile, so `ECHO "Add build steps here"` is all that is needed.

Now, let's go through the YAML file section by section:

- The `on` section specifies when the workflow should run. This is not relevant for our bash and Docker setup, so we can ignore it.

- The `jobs` section contains the actual build steps. We will need to adapt these steps for our `build.sh` and `build.Dockerfile` files.

  - The `actions/checkout@v3` step is not needed, as our `run.sh` and `build.sh` scripts will be stored in the git repository along with the code.

  - The "Build the Docker image" step should be included in the `run.sh`.

  - Since that is all the steps in the file, we conclude that  `build.Dockerfile` won't need any dependencies installed and `build.sh` will only contain an echo to indicate where build steps should be placed.

`run.sh`:

```bash
#!/bin/bash

# Build the Docker image
IMAGE_NAME="my-image-name"
TAG=$(date +%s)

# Build the application Docker image
docker build . --file Dockerfile --tag $IMAGE_NAME:$TAG
```

`build.Dockerfile`:
```
# Use a alpine base image
FROM alpine:latest

# Set the working directory
WORKDIR /app

# Copy the build.sh script into the image
COPY build.sh ./
```

`build.sh`:
```bash
#!/bin/bash

# Place to insert customized build steps
echo "Add build steps here!"
```