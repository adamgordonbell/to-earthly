VERSION 0.7

all:
  BUILD +docker

docker:
  FROM alpine:latest
  CMD ["/bin/sh"]
  SAVE IMAGE --push my-image:$(date +%s)