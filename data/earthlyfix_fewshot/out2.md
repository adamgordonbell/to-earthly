VERSION 0.7

build:
    FROM alpine
    RUN head -c 1M </dev/urandom >file.txt
    SAVE ARTIFACT file.txt

another:
    FROM debian:buster-slim
    COPY +build/file.txt .
    SAVE IMAGE --push bla