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

These three files are created as requested. The `run.sh` script is responsible for building the application Docker image, while the `build.Dockerfile` sets up a minimal environment with the `build.sh` script. The `build.sh` script is a placeholder for any additional build steps that may be required.