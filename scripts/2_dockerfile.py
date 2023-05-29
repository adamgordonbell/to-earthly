from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

from core import io, prompts

inputfolder: str = 'test_cases/node_server/input'
outputfolder: str = 'test_cases/node_server/output'

outputfile: str = f'{outputfolder}/Dockerfile'

def main() -> None:
    yml :str  = io.find_first_yml(inputfolder)
  
    summarize : str = prompts.summarize_gha(yml)

    filestructure = io.run_tree(inputfolder)
    extra_docker_file = io.find_first_dockerfile(inputfolder)
    result = prompts.create_dockerfile(filestructure, summarize, extra_docker_file)
    print("Result:\n\n")
    print(result)

if __name__ == '__main__':
    main()