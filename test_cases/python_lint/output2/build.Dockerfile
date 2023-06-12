# Use a Python 3.10 base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and the src directory
COPY requirements.txt .
COPY src/ src/

# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install flake8 pytest
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copy the build.sh script into the image
COPY build.sh ./