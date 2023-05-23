from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

# from core.io import write_sections
from core.prompts import summarize_gha, create_dockerfile, create_earthfile
from core.io import write, find_first_yml, run_tree

inputfolder: str = 'test_cases/python_lint/input'
outputfolder: str = 'test_cases/python_lint/output'

# inputfolder: str = 'test_cases/docker_simple/input'
# outputfolder: str = 'test_cases/docker_simple/output'

def main() -> None:
    yml = find_first_yml(inputfolder)
    file_structure = run_tree(inputfolder)
    write(file_structure,f"{outputfolder}/files.txt")

    summarize : str = summarize_gha(yml)
    write(summarize,f"{outputfolder}/summary.md")

    dockerfile = create_dockerfile(file_structure, summarize)
    write(dockerfile,f"{outputfolder}/Dockerfile")

    earthfile = create_earthfile(dockerfile)
    write(earthfile,f"{outputfolder}/Earthfile")

if __name__ == '__main__':
    main()