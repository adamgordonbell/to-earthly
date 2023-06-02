To approach this problem, we will follow these steps:

1. Analyze the given files and understand the build process.
2. Create an Earthfile with the necessary targets.
3. Port the steps from the Dockerfile and bash scripts to the Earthfile targets.

Now, let's go through the files step by step and discuss how the steps should be ported to Earthly.

`Files`:
The file structure consists of a `Dockerfile`, `Earthfile`, `index.html`, `output2/`, `package-lock.json`, `package.json`, `postcss.config.cjs`, `public/`, `src/`, `tailwind.config.cjs`, `tsconfig.json`, `tsconfig.node.json`, `vite.config.ts`, and `yarn.lock`. We will need to copy these files into the Earthfile at the appropriate stages.

`run.sh`:
This script clones the repository, logs in to Docker Hub, builds the Docker image, pushes the Docker image, and runs the build process inside the Docker container. In Earthly, we don't need to wrap Docker commands in a bash script. Instead, we will create targets in the Earthfile to handle the build process.

`build.Dockerfile`:
This Dockerfile sets up the base image, working directory, copies files, installs dependencies, and sets the `build.sh` script as executable. We will create a `base` target in the Earthfile to handle these steps.

`build.sh`:
This script sets environment variables and runs the React build process. We will create a `build` target in the Earthfile to handle these steps.

Here's how the Earthfile targets should look like:

1. Header
   - The header of the Earthfile starts with a version declaration. `VERSION 0.7`
   - Then pick the base image. Node 19 in this case.
   - Set the working directory to `/app`.
 
2. `deps` target:
   - Copy the `package*.json` files.
   - Install TypeScript globally.
   - Run `npm ci`.
   - Copy the remaining files and directories.

3. `build` target:
   - Use the `deps` target as a starting point.
   - Set the environment variables.
   - Run the React build process with `npm run build`.

4. `all` target:
Earthfiles often have an `all` target that is run in CI or by a developer and covers all actions.
   - Build the `build` target with BUILD `+build` syntax.

Note that the Earthfile does not handle the Docker Hub login, image push, and repository cloning steps. These steps should be handled in your CI/CD pipeline or a separate script. The Earthfile focuses on the build process itself.