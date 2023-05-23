## Files
```
.
├── Dockerfile
└── file1.txt
```

## Build Steps
```
Steps:
   - Build the Docker image: `docker build . --file Dockerfile --tag my-image:$(date +%s)`
```

## Existing Dockerfile
```
FROM alpine:latest
COPY ./file1.txt .
CMD ["/bin/sh"]
```
