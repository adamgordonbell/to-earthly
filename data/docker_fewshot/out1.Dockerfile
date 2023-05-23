FROM python:3.10 AS base

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install pytest
RUN pip install -r requirements.txt

FROM base AS test
COPY hello.py .
RUN pytest

FROM alpine:latest as docker
COPY ./file1.txt .
CMD ["/bin/sh"]
SAVE IMAGE --push my-image:$(date +%s)