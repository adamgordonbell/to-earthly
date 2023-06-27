VERSION 0.7
FROM python:3.11
WORKDIR /app

deps:
  RUN apt-get update && apt-get install -y tree
  COPY requirements.txt .
  RUN python -m pip install --upgrade pip
  RUN pip install pytest
  RUN pip install -r requirements.txt

docker:
  FROM +deps
  COPY --dir core data scripts util .
  COPY __init__.py .
  ENV PYTHONPATH=/app:$PYTHONPATH
  CMD ["python", "./scripts/run.py", "--input_dir", "/input", "--output_dir", "/input/.to_earthly/", "--earthfile", "/input/Earthfile"]
  SAVE IMAGE --push agbell/to-earthly