from typing import List, Optional, Callable
from pprint import pprint

# from core.io import write_sections
from core.prompts import summarize_gha
from core.io import write

inputfile: str = 'data/python4/workflow.yml'
outputfile: str = 'data/python4/summary.md'

def main() -> None:
    with open(inputfile, 'r') as infile:
        document: str = infile.read()
    summarize : str = summarize_gha(document)
    write(summarize, outputfile)

if __name__ == '__main__':
    main()