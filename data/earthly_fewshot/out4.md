VERSION 0.7
FROM golang:1.17
WORKDIR /go-example

all:
  BUILD +build
  BUILD +docker

deps:
    COPY go.mod go.sum ./
    RUN go mod download
    SAVE ARTIFACT go.mod
    SAVE ARTIFACT go.sum

build:
    FROM +deps
    COPY +deps/go.mod .
    COPY +deps/go.sum .
    COPY main.go .
    RUN go build -o build/go-example main.go
    SAVE ARTIFACT build/go-example /go-example

docker:
    COPY +build/go-example .
    ENTRYPOINT ["/go-example/go-example"]
    SAVE IMAGE --push go-example