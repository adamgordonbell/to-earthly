# Use a alpine base image
FROM alpine:latest

# Set the working directory
WORKDIR /app

# Copy the build.sh script into the image
COPY build.sh ./