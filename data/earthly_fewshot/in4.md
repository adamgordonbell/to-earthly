FROM golang:1.17 as base
WORKDIR /go-example

COPY go.mod go.sum ./
RUN go mod download

FROM golang:1.17 as build
COPY --from=base go.mod go.sum .
RUN go build -o build/go-example main.go

FROM debian:buster-slim as docker
COPY --from=build /go-example .
ENTRYPOINT ["/go-example/go-example"]
SAVE IMAGE --push go-example