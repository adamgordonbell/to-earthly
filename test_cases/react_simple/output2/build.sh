#!/bin/bash

# Set environment variables
export VITE_RUST_SERVER=http://localhost:8000
export VITE_GO_SERVER=http://localhost:8001
export VITE_PYTHON_SERVER=http://localhost:8002
export VITE_NODE_SERVER=http://localhost:8003

# Run the React build process
npm run build
