FROM node:19 AS base

WORKDIR /app

COPY package.json .
COPY tsconfig.json .
COPY tsconfig.node.json .
COPY postcss.config.cjs .
COPY tailwind.config.cjs .
COPY vite.config.ts .
COPY public/ ./public
COPY index.html .
COPY src/ ./src

RUN npm install -g typescript
RUN npm install

FROM base AS build
ENV VITE_RUST_SERVER=http://localhost:8000
ENV VITE_GO_SERVER=http://localhost:8001
ENV VITE_PYTHON_SERVER=http://localhost:8002
ENV VITE_NODE_SERVER=http://localhost:8003
RUN npm run build

FROM node:19 AS final
COPY --from=build /app /app
EXPOSE 5173
ENTRYPOINT [ "npm", "run", "dev", "--host"]
SAVE IMAGE --push ezeev/earthly-react-example:gh-actions-only