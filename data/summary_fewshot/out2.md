Preconditions:
- Install Python 3.10
- Install pip

Steps:
   - Install dependencies:
     - `python -m pip install --upgrade pip`
     - `pip install pylint`
   - Analysing the code with pylint: `pylint $(git ls-files '*.py')`