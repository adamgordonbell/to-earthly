from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

# from core.io import write_sections
from core.prompts import summarize_gha, create_dockerfile, create_earthfile
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
    dockerfile = create_dockerfile(filestructure, summarize)
    earthfile = create_earthfile(dockerfile)
    print(earthfile)

if __name__ == '__main__':
    main()