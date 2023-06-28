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
  COPY --dir toearthly .
  ENV PYTHONPATH=/app:$PYTHONPATH
  CMD ["python", "/app/toearthly/scripts/run.py", "--input_dir", "/input", "--output_dir", "/input/.to_earthly/", "--earthfile", "/input/Earthfile"]
  SAVE IMAGE to-earthly