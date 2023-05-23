FROM alpine:latest

COPY readme.txt /app/readme.txt

RUN docker build . --file Dockerfile --tag my-image-name:$(date +%s)