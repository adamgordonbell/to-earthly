# Use a Node.js 19 alpine base image
FROM node:19-alpine

# Set the working directory
WORKDIR /app

# Copy the build.sh script into the image
COPY build.sh ./

# Install global dependencies
RUN npm install -g typescript