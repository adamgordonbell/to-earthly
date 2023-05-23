FROM alpine:latest
CMD ["/bin/sh"]
SAVE IMAGE --push my-image:$(date +%s)