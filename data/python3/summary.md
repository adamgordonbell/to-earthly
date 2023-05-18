1. Install dependencies:
```bash
python -m pip install --upgrade pip
pip install pylint
```

2. Analyze the code with pylint:
```bash
pylint $(git ls-files '*.py')
```