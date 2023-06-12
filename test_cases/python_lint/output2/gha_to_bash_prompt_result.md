`run.sh`:

```bash
#!/bin/bash

# Build the Docker image
docker build -t build -f build.Dockerfile .

# Run the build.sh script inside the Docker container
docker run --rm build ./build.sh
```

`build.Dockerfile`:

```
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
```

`build.sh`:

```bash
#!/bin/bash

# Lint with flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Test with pytest
pytest
```