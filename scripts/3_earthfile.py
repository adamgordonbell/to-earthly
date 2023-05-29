from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

from core import io, prompts

# inputfolder: str = 'test_cases/python_lint/input'
# outputfolder: str = 'test_cases/python_lint/output'

# inputfolder: str = 'test_cases/react_simple/input'
# outputfolder: str = 'test_cases/react_simple/output'

inputfolder: str = 'test_cases/docker_simple/input'
outputfolder: str = 'test_cases/docker_simple/output'

def main() -> None:
    yml = io.find_first_yml(inputfolder)
    file_structure = io.run_tree(inputfolder)
    io.write(file_structure,f"{outputfolder}/files.txt")

    summarize : str = prompts.summarize_gha(yml)
    io.write(summarize,f"{outputfolder}/summary.md")

    extra_docker_file = io.find_first_dockerfile(inputfolder)
    dockerfile = prompts.create_dockerfile(file_structure, summarize, extra_docker_file)
    io.write(dockerfile,f"{outputfolder}/Dockerfile")

    earthfile = prompts.create_earthfile(dockerfile)
    io.write(earthfile,f"{outputfolder}/Earthfile")

    earthfile = prompts.fix_earthfile(earthfile)
    io.write(earthfile,f"{outputfolder}/Earthfile.fix")

    earthfile = prompts.create_earthfile_cot(earthfile)
    io.write(earthfile,f"{outputfolder}/Earthfile.cot")

if __name__ == '__main__':
    main()