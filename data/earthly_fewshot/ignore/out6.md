VERSION 0.7
FROM node:19
WORKDIR /app

all:
  BUILD +build
  BUILD +final

base:
  COPY *.json .
  COPY --dir src public .
  RUN npm install -g typescript
  RUN npm install

build:
  FROM +base
  RUN npm run build
  SAVE ARTIFACT /dist

final:
  FROM node:19.5.0-buster-slim
  COPY +build/dist .
  EXPOSE 5173
  ENTRYPOINT [ "npm", "run", "dev", "--host"]
  SAVE IMAGE --push image1