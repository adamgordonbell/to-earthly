To approach this problem, we will follow these steps:

1. Analyze the given files and understand the build process.
2. Create an Earthfile with the necessary targets.
3. Port the steps from the Dockerfile and bash scripts to the Earthfile targets.

Now, let's go through the files step by step and discuss how the steps should be ported to Earthly.

`Files`:
The file structure consists of a `Dockerfile`, `Earthfile`, `index.html`, `output2/`, `package-lock.json`, `package.json`, `postcss.config.cjs`, `public/`, `src/`, `tailwind.config.cjs`, `tsconfig.json`, `tsconfig.node.json`, `vite.config.ts`, and `yarn.lock`. We will need to copy these files into the Earthfile at the appropriate stages.

`run.sh`:
This script logs into Docker Hub, builds the Docker image, runs the `build.sh` script inside the Docker container, and then builds and pushes the application Docker image. In Earthly, we don't need to wrap Docker commands in a bash script. Instead, we will create targets in the Earthfile to handle the build process.

`build.Dockerfile`:
This Dockerfile sets up the base image, working directory, copies the `build.sh` script, and installs global dependencies. We will create a `base` target in the Earthfile to handle these steps.

`build.sh`:
This script copies the necessary files into the container, installs local dependencies, and runs the React Service Build. We will create separate targets in the Earthfile for copying files, installing dependencies, and building the React application.

Here's how the Earthfile targets should look like:

1. Header
   - The header of the Earthfile starts with a version declaration. `VERSION 0.7`
   - Then pick the base image. Node.js 19 alpine in this case.
   - Set the working directory to `/app`.

2. `base` target:
   - Copy the `build.sh` script into the image.
   - Install global dependencies using npm.

3. `copy-files` target:
   - Use the `base` target as a starting point.
   - Copy the necessary files and directories into the Earthfile.

4. `install-deps` target:
   - Use the `copy-files` target as a starting point.
   - Install local dependencies using npm.

5. `build` target:
   - Use the `install-deps` target as a starting point.
   - Run the React Service Build with the appropriate environment variables.

6. `all` target:
   - Earthfiles often have an `all` target that is run in CI or by a developer and covers all actions.
   - Build the `build` target with the BUILD `+target` syntax.