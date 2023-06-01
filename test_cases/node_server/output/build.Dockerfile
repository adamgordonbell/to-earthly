# Use the desired Node.js version
FROM node:19

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Grant execute permission to the build script
RUN chmod +x build.sh
