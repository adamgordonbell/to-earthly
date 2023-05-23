Preconditions:
- Install Docker
- Install Node.js 19.x
- Set environment variables:
  - DOCKERHUB_USERNAME
  - DOCKERHUB_TOKEN

Steps:
   1. Log in to Docker Hub: `docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN`
   2. Build and push Docker image: `docker build . -t ezeev/earthly-react-example:gh-actions-only && docker push ezeev/earthly-react-example:gh-actions-only`
   3. Cache node_modules (optional, for faster builds): `tar -czf node_modules.tar.gz node_modules`
   4. Install global dependencies: `npm install -g typescript`
   5. Install local dependencies: `npm install`
   6. Build React service:
      ```
      export VITE_RUST_SERVER=http://localhost:8000
      export VITE_GO_SERVER=http://localhost:8001
      export VITE_PYTHON_SERVER=http://localhost:8002
      export VITE_NODE_SERVER=http://localhost:8003
      npm run build
      ```