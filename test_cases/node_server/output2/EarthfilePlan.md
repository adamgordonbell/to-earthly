To approach this problem, we will follow these steps:

1. Analyze the given files and understand the build process.
2. Create an Earthfile with the necessary targets.
3. Port the steps from the Dockerfile and bash scripts to the Earthfile targets.

Now, let's go through the files step by step and discuss how the steps should be ported to Earthly.

`Files`:
The file structure consists of a `Dockerfile`, `Earthfile`, `package-lock.json`, `package.json`, `quotes.txt`, and a `src` directory containing `index.js`, `quotes.js`, and `quotes.test.js`. We will need to copy these files into the Earthfile at the appropriate stages.

`run.sh`:
This script logs into Docker Hub, builds the Docker image, and pushes the image to Docker Hub. In Earthly, we don't need to wrap Docker commands in a bash script. Instead, we will create targets in the Earthfile to handle the build process.

`build.Dockerfile`:
This Dockerfile sets up the base image, working directory, copies files, and installs dependencies. We will create a `base` target in the Earthfile to handle these steps.

`build.sh`:
This script installs the npm packages and runs the tests. We will create separate targets in the Earthfile for installing dependencies and running tests.

Here's how the Earthfile targets should look like:

1. Header
   - The header of the Earthfile starts with a version declaration. `VERSION 0.7`
   - Then pick the base image. Node 19 in this case.
   - Set the working directory to `/app`.
 
2. `deps` target:
   - Copy the `package.json` and `package-lock.json` files.
   - Run `npm install`.

3. `test` target:
   - Use the `deps` target as a starting point.
   - Copy the `src` directory and `quotes.txt` file.
   - Run `npm test`.

4. `all` target:
Earthfiles often have an `all` target that is run in CI or by a developer and covers all actions.
   - Build `test` target with BUILD `+target` syntax

5. `docker-push` target (optional):
   - If you want to push the built image to Docker Hub, you can create a `docker-push` target.
   - Use the `all` target as a starting point.
   - Set the Docker Hub username and token as environment variables.
   - Log in to Docker Hub.
   - Build and push the Docker image.

Note: The `docker-push` target is optional and should be used with caution, as it requires handling sensitive information like Docker Hub credentials.