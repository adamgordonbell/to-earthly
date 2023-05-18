from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

# from core.io import write_sections
from core.prompts import summarize_gha, create_dockerfile
from core.io import write

inputfile: str = 'data/python3/workflow.yml'
outputfile: str = 'data/python3/Dockerfile'

def main() -> None:
    with open(inputfile, 'r') as infile:
        document: str = infile.read()
  
    summarize : str = summarize_gha(document)

    filestructure = dedent("""
    .
    ├── Earthfile
    ├── requirements.txt
    └── src
        └── hello.py
    """)
    result = create_dockerfile(filestructure, summarize)
    print("Result:\n\n")
    print(result)

if __name__ == '__main__':
    main()