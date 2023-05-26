from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

# from core.io import write_sections
from core.prompts import summarize_gha, create_dockerfile, create_earthfile, fix_earthfile
from core.io import write, find_first_yml, run_tree, find_first_dockerfile

# inputfolder: str = 'test_cases/python_lint/input'
# outputfolder: str = 'test_cases/python_lint/output'

inputfolder: str = 'test_cases/react_simple/input'
outputfolder: str = 'test_cases/react_simple/output'

# inputfolder: str = 'test_cases/docker_simple/input'
# outputfolder: str = 'test_cases/docker_simple/output'

def main() -> None:
    yml = find_first_yml(inputfolder)
    file_structure = run_tree(inputfolder)
    write(file_structure,f"{outputfolder}/files.txt")

    summarize : str = summarize_gha(yml)
    write(summarize,f"{outputfolder}/summary.md")

    extra_docker_file = find_first_dockerfile(inputfolder)
    dockerfile = create_dockerfile(file_structure, summarize, extra_docker_file)
    write(dockerfile,f"{outputfolder}/Dockerfile")

    earthfile = create_earthfile(dockerfile)
    write(earthfile,f"{outputfolder}/Earthfile")

    earthfile = fix_earthfile(earthfile)
    write(earthfile,f"{outputfolder}/Earthfile.fix")

if __name__ == '__main__':
    main()