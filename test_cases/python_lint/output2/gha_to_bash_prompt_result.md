Here are the `run.sh`, `build.Dockerfile`, and `build.sh` files:

`run.sh`:
```bash
#!/bin/bash

# Build the Docker image
docker build -t python-build -f build.Dockerfile .

# Run the build.sh script inside the Docker container
docker run --rm python-build ./build.sh
```

`build.Dockerfile`:
```Dockerfile
FROM python:3.10

WORKDIR /app

# Copy necessary files
COPY requirements.txt .
COPY src/ src/

# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install flake8 pytest
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copy build.sh script
COPY build.sh .

# Set build.sh as executable
RUN chmod +x build.sh
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

To run the build process, execute the `run.sh` script. This will build the Docker image using `build.Dockerfile` and then run the `build.sh` script inside the Docker container. The `build.sh` script will perform linting with flake8 and run tests with pytest.