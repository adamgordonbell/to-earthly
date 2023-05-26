FROM node:19 AS base

WORKDIR /app

COPY *.json .
COPY public/ ./public
COPY src/ ./src

RUN npm install -g typescript
RUN npm install

FROM base AS build
RUN npm run build

FROM node:19.5.0-buster-slim AS final

WORKDIR /app
COPY --from=build /app/dist .

EXPOSE 5173
ENTRYPOINT [ "npm", "run", "dev", "--host"]

SAVE IMAGE --push image1