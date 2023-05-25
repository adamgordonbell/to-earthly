FROM gcc:latest AS builder
WORKDIR /app
COPY hello.c .
RUN gcc -o hello hello.c

FROM debian:buster-slim
COPY --from=builder /app/hello /usr/local/bin
CMD ["/usr/local/bin/hello"]
SAVE IMAGE my-image