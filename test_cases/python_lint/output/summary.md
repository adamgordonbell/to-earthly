Preconditions:
- Install Python 3.10
- Install pip

Steps:
   - Install dependencies:
     - `python -m pip install --upgrade pip`
     - `pip install flake8 pytest`
     - `if [ -f requirements.txt ]; then pip install -r requirements.txt; fi`
   - Lint with flake8:
     - `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
     - `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`
   - Test with pytest: `pytest`