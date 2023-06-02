Here are the `run.sh`, `build.Dockerfile`, and `build.sh` files:

`run.sh`:
```bash
#!/bin/bash
DOCKERHUB_USERNAME=<your_dockerhub_username>
DOCKERHUB_TOKEN=<your_dockerhub_token>

docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN
docker build -t ezeev/earthly-node-example:gh-actions-only -f build.Dockerfile .
docker push ezeev/earthly-node-example:gh-actions-only
```

`build.Dockerfile`:
```Dockerfile
FROM node:19
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
```

`build.sh`:
```bash
#!/bin/bash
npm install
npm test
```

Remember to replace `<your_dockerhub_username>` and `<your_dockerhub_token>` with your actual Docker Hub credentials in `run.sh`. Also, make sure to copy the necessary files (e.g., `package.json`, `package-lock.json`, and source code) into the Docker image in the `build.Dockerfile`.