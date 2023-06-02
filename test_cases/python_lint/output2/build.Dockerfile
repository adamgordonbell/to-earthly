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
