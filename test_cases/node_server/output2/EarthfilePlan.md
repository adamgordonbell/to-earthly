To approach this problem, we will follow these steps:

1. Analyze the given files and understand the build process.
2. Create an Earthfile with the necessary targets.
3. Port the steps from the Dockerfile and bash scripts to the Earthfile targets.

Now, let's go through the files step by step and discuss how the steps should be ported to Earthly.

`Files`:
The file structure consists of a `package.json`, `package-lock.json`, `quotes.txt`, and a `src` directory containing JavaScript files. We will need to copy these files into the Earthfile at the appropriate stages.

`run.sh`:
This script builds the Docker image, runs the `build.sh` script inside the Docker container, and pushes the Docker image. In Earthly, we don't need to wrap Docker commands in a bash script. Instead, we will create targets in the Earthfile to handle the build process.

`build.Dockerfile`:
This Dockerfile sets up the base image, working directory, copies files, installs dependencies, and sets the `build.sh` script as executable. We will create a `base` target in the Earthfile to handle these steps.

`build.sh`:
This script runs the Node.js build and tests. We will create separate targets in the Earthfile for building and testing.

Here's how the Earthfile targets should look like:

1. Header
   - The header of the Eartfile starts with a version declaration. `VERSION 0.7`
   - Then pick the base image. Node 19 in this case.
   - Set the working directory to `/app`.
 
2. `deps` target:
   - Copy the `package.json` and `package-lock.json` files.
   - Install dependencies using `npm ci`.
   - Copy the `src` directory and `quotes.txt` file.

3. `build` target:
   - Use the `deps` target as a starting point.
   - Run `npm install` to build the project.

4. `test` target:
   - Use the `build` target as a starting point.
   - Run `npm test` for testing.

5. `all` target:
Earthfiles often have an `all` target that is run in CI or by a developer and covers all actions.
   - Build `test` target with BUILD `+test` syntax

Here's the Earthfile based on the given files:

```
VERSION 0.7
FROM node:19
WORKDIR /app

deps:
  COPY package*.json ./
  RUN npm ci
  COPY src/ src/
  COPY quotes.txt .

build:
  FROM +deps
  RUN npm install

test:
  FROM +build
  RUN npm test

all:
  BUILD +test
```