from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

from core import io, prompts

inputfolder: str = '/input'

def main() -> None:
    yml = io.find_first_yml(inputfolder)
    file_structure = io.run_tree(inputfolder)

    summarize : str = prompts.summarize_gha(yml)

    extra_docker_file = io.find_first_dockerfile(inputfolder)
    dockerfile = prompts.create_dockerfile(file_structure, summarize, extra_docker_file)

    earthfile = prompts.create_earthfile(dockerfile)
    earthfile = prompts.fix_earthfile(dockerfile)
    io.write(earthfile,f"{inputfolder}/Earthfile")

if __name__ == '__main__':
    main()