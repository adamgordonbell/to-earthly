To recreate the steps of this GitHub Actions workflow using bash and Docker, we will modify the `run.sh` script to build the Docker image and push it to a container registry. We will also need to update the `build.Dockerfile` to include the necessary steps for building the application Docker image.

Here's how the files should look like:

`run.sh`:
```bash
#!/bin/bash

# Build the Docker image
IMAGE_NAME="my-image-name"
TAG=$(date +%s)
docker build . --file build.Dockerfile --tag $IMAGE_NAME:$TAG

# Run the build.sh script inside the Docker container
docker run --rm $IMAGE_NAME:$TAG ./build.sh

# Build the application Docker image
docker build . --file Dockerfile --tag $IMAGE_NAME:$TAG

# Push the Docker image to a container registry (optional)
# docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
# docker push $IMAGE_NAME:$TAG
```

`build.Dockerfile`:
```Dockerfile
# Use the Python 3.10 base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and the src directory
COPY requirements.txt .
COPY src/ src/

# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install flake8 pytest
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Set the build.sh script as executable
COPY build.sh .
RUN chmod +x build.sh
```

`build.sh`:
```bash
#!/bin/bash

# Run linting with flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run testing with pytest
pytest
```

Make sure to give execute permissions to the `run.sh` and `build.sh` scripts by running `chmod +x run.sh` and `chmod +x build.sh`. Then, you can execute the `run.sh` script to build and run the Docker container.