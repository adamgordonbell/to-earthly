To recreate the steps of this GitHub Actions workflow using `run.sh`, `build.Dockerfile`, and `build.sh`, we will follow these steps:

1. Analyze the given GitHub Actions workflow YAML file and understand the build process.
2. Create `run.sh`, `build.Dockerfile`, and `build.sh` files to handle the build process.

Now, let's go through the YAML file step by step and discuss how the steps should be ported to the new format.

`GitHub Actions workflow YAML`:

1. Checkout the code: This step is not needed in `run.sh`, `build.Dockerfile`, or `build.sh` because these files are stored in the git repository along with the code.

2. Docker login: This step should be included in `run.sh`. Add the following line to `run.sh`:
   ```
   docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN
   ```

3. Docker build and push: This step should be included in `run.sh`. Add the following lines to `run.sh`:
   ```
   docker build -t ezeev/earthly-node-example:gh-actions-only -f build.Dockerfile .
   docker push ezeev/earthly-node-example:gh-actions-only
   ```

4. Cache node_modules: This step is not needed in `run.sh`, `build.Dockerfile`, or `build.sh` because caching is handled by Docker.

5. Setup Node.js: This step should be included in `build.Dockerfile`. Add the following lines to `build.Dockerfile`:
   ```
   FROM node:19
   WORKDIR /app
   ```

6. Node Service Build: This step should be included in `build.sh`. Add the following line to `build.sh`:
   ```
   npm install
   ```

7. Node Service Test: This step should be included in `build.sh`. Add the following line to `build.sh`:
   ```
   npm test
   ```

`run.sh`:
```
#!/bin/bash
DOCKERHUB_USERNAME=<your_dockerhub_username>
DOCKERHUB_TOKEN=<your_dockerhub_token>

docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN
docker build -t ezeev/earthly-node-example:gh-actions-only -f build.Dockerfile .
docker push ezeev/earthly-node-example:gh-actions-only
```

`build.Dockerfile`:
```
FROM node:19
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
```

`build.sh`:
```
#!/bin/bash
npm install
npm test
```

Remember to replace `<your_dockerhub_username>` and `<your_dockerhub_token>` with your actual Docker Hub credentials in `run.sh`.