VERSION 0.7
FROM python:3.9
WORKDIR /app

all:
  BUILD +analyze

deps:
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY src/ src/

build:
  FROM +deps
  RUN pip install pylint pytest

analyze:
  FROM +build
  RUN pylint $(find src/ -name '*.py')
  RUN pytest