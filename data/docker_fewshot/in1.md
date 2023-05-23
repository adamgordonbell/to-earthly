## Files
```
.
├── hello.py
├── Dockerfile
└── file1.txt
```

## Build Steps
```
Preconditions:
- Install Python 3.10
- Install pip

Steps:
   - Install dependencies:
     - `python -m pip install --upgrade pip`
     - `pip install pytest`
     - `pip install -r requirements.txt`
   - Test with pytest: `pytest`
   - Build the Docker image: `docker build . --file Dockerfile --tag my-image:$(date +%s)`
```

## Existing Dockerfile
```
FROM alpine:latest
COPY ./file1.txt .
CMD ["/bin/sh"]
```
