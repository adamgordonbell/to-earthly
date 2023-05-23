FROM alpine:latest

COPY readme.txt /app/readme.txt

RUN echo "Install Docker" && \
    apk add --no-cache docker

RUN echo "Build the Docker image" && \
    docker build . --file Dockerfile --tag my-image-name:$(date +%s)