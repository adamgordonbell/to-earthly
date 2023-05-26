VERSION 0.7
FROM alpine:3.15

build:
    RUN echo "word" > ./a-file

another:
    FROM busybox
    COPY +build/a-file .