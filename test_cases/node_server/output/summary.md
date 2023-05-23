Preconditions:
- Install Docker
- Install Node.js 19.x
- Set environment variables: DOCKERHUB_USERNAME and DOCKERHUB_TOKEN

Steps:
1. Docker login: `docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN`
2. Build and push Docker image: `docker build -t ezeev/earthly-node-example:gh-actions-only . && docker push ezeev/earthly-node-example:gh-actions-only`
3. Cache node_modules (optional): `tar -czf node_modules.tar.gz node_modules`
4. Install Node.js dependencies: `npm install`
5. Run Node.js tests: `npm test`