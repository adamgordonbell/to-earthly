FROM python:3.9 AS base

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install flake8 pytest
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

FROM base AS lint

COPY src/ .

RUN flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
RUN flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

FROM base AS test

COPY src/ .

RUN pytest