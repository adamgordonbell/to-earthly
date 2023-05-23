from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

# from core.io import write_sections
from core.prompts import summarize_gha, create_dockerfile
from core.io import write, run_tree, find_first_yml

inputfolder: str = 'test_cases/docker_simple/input'
outputfolder: str = 'test_cases/docker_simple/output'

outputfile: str = f'{outputfolder}/Dockerfile'

def main() -> None:
    yml :str  = find_first_yml(inputfolder)
  
    summarize : str = summarize_gha(yml)

    filestructure = run_tree(inputfolder)
    result = create_dockerfile(filestructure, summarize)
    print("Result:\n\n")
    print(result)

if __name__ == '__main__':
    main()