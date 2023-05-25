VERSION 0.7

all:
  BUILD +docker

builder:
  FROM gcc:latest AS builder
  WORKDIR /app
  COPY hello.c .
  RUN gcc -o hello hello.c
  SAVE ARTIFACT hello

docker:
  FROM alpine:latest
  COPY +build/hello /usr/local/bin
  CMD ["/usr/local/bin/hello"]
  SAVE IMAGE my-image