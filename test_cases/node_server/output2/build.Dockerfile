# Use a Node.js base image
FROM node:19

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the source code
COPY . .

# Copy the build.sh script into the image
COPY build.sh ./