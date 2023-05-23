FROM node:19-alpine3.16 AS base

WORKDIR /app
COPY package.json ./
COPY src/ ./src
RUN npm install
COPY quotes.txt ./quotes.txt

FROM base AS test
RUN npm test

FROM base AS final
EXPOSE 8003
ENTRYPOINT [ "node", "src/index.js" ]

# Save the image and push to Docker Hub
SAVE IMAGE --push ezeev/earthly-node-example:gh-actions-only