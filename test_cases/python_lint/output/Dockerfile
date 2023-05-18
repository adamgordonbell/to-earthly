FROM python:3.10 AS base

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install flake8 pytest && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

COPY src/ .

RUN flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && \
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

RUN pytest