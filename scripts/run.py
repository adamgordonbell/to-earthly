from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent

from core.prompts import summarize_gha, create_dockerfile, create_earthfile, fix_earthfile
from core.io import write, find_first_yml, run_tree, find_first_dockerfile

inputfolder: str = '/input'

def main() -> None:
    yml = find_first_yml(inputfolder)
    file_structure = run_tree(inputfolder)

    summarize : str = summarize_gha(yml)

    extra_docker_file = find_first_dockerfile(inputfolder)
    dockerfile = create_dockerfile(file_structure, summarize, extra_docker_file)

    earthfile = create_earthfile(dockerfile)
    earthfile = fix_earthfile(dockerfile)
    write(earthfile,f"{inputfolder}/Earthfile")

if __name__ == '__main__':
    main()