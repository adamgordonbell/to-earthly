#!/bin/bash

# Copy the necessary files into the container
cp -r /app .

# Install local dependencies
npm install

# Run the React Service Build
VITE_RUST_SERVER=http://localhost:8000 \
VITE_GO_SERVER=http://localhost:8001 \
VITE_PYTHON_SERVER=http://localhost:8002 \
VITE_NODE_SERVER=http://localhost:8003 \
npm run build