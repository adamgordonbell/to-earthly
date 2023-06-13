# Use an official nginx image as a parent image
FROM nginx:latest

# Set working directory in the container
WORKDIR /usr/share/nginx/html

# Copy the specific file you want to include in the container
COPY ./readme.txt .

# Expose port 80
EXPOSE 80

# Start Nginx when the container has provisioned.
CMD ["nginx", "-g", "daemon off;"]
