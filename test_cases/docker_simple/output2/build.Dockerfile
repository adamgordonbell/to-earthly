# Use the Python 3.10 base image
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

# Set the build.sh script as executable
COPY build.sh .
RUN chmod +x build.sh

# Run the build.sh script
CMD ["./build.sh"]
