VERSION 0.7

build:
    FROM alpine
    RUN head -c 1M </dev/urandom >file.txt

another:
    FROM debian:buster-slim
    COPY +build/file .
    SAVE IMAGE --push bla