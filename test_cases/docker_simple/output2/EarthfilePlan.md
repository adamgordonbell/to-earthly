To approach this problem, we will follow these steps:

1. Analyze the given files and understand the build process.
2. Create an Earthfile with the necessary targets.
3. Port the steps from the Dockerfile and bash scripts to the Earthfile targets.

Now, let's go through the files step by step and discuss how the steps should be ported to Earthly.

`Files`:
The file structure consists of a `Dockerfile` and a `readme.txt` file. We will need to copy these files into the Earthfile at the appropriate stages.

`run.sh`:
This script builds the Docker image using the `Dockerfile`. In Earthly, we don't need to wrap Docker commands in a bash script. Instead, we will create targets in the Earthfile to handle the build process.

`build.Dockerfile`:
This Dockerfile sets up the base image (Alpine), working directory, and copies the `build.sh` script into the image. We will create a `base` target in the Earthfile to handle these steps.

`build.sh`:
This script is a placeholder for customized build steps. We will create a `build` target in the Earthfile to handle these steps.

Here's how the Earthfile targets should look like:

1. Header
   - The header of the Earthfile starts with a version declaration. `VERSION 0.7`
   - Then pick the base image. Alpine in this case.
   - Set the working directory to `/app`.
 
2. `base` target:
   - Copy the `Dockerfile` and `readme.txt` files.
   - Copy the `build.sh` script and make it executable.

3. `build` target:
   - Use the `base` target as a starting point.
   - Run the `build.sh` script.

4. `all` target:
Earthfiles often have an `all` target that is run in CI or by a developer and covers all actions.
   - Build the `build` target with BUILD `+target` syntax.

Here's the Earthfile based on the given files:

```
VERSION 0.7
FROM alpine:latest
WORKDIR /app

base:
  COPY Dockerfile .
  COPY readme.txt .
  COPY build.sh .
  RUN chmod +x build.sh

build:
  FROM +base
  RUN ./build.sh

all:
  BUILD +build
```

This Earthfile represents the build process described in the given files and combines the concepts of running bash commands to build something with the ideas of containerization made popular by Docker and Dockerfile.