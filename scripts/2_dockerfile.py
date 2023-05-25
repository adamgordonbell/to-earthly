from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

# from core.io import write_sections
from core.prompts import summarize_gha, create_dockerfile
from core.io import write, run_tree, find_first_yml, find_first_dockerfile

inputfolder: str = 'test_cases/node_server/input'
outputfolder: str = 'test_cases/node_server/output'

outputfile: str = f'{outputfolder}/Dockerfile'

def main() -> None:
    yml :str  = find_first_yml(inputfolder)
  
    summarize : str = summarize_gha(yml)

    filestructure = run_tree(inputfolder)
    extra_docker_file = find_first_dockerfile(inputfolder)
    result = create_dockerfile(filestructure, summarize, extra_docker_file)
    print("Result:\n\n")
    print(result)

if __name__ == '__main__':
    main()