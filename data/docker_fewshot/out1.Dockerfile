FROM alpine:latest
COPY ./file1.txt .
CMD ["/bin/sh"]
SAVE IMAGE --push my-image:$(date +%s)