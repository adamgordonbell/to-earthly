from typing import List, Optional, Callable
from pprint import pprint

from core import io, prompts, gha_to_bash_prompt

inputfolder: str = 'test_cases/node_server/input/'
outputfolder: str = 'test_cases/node_server/output/'

def main() -> None:
    print("Gather Data")
    yml = io.find_first_yml(inputfolder)
    file_structure = io.run_tree(inputfolder)
    io.write(file_structure,outputfolder + "files.txt")

    print("Running Stage 1")
    runfile, dockerfile, buildfile = gha_to_bash_prompt.prompt1(yml)
    io.write(runfile, outputfolder + "run.sh")
    io.write(dockerfile, outputfolder + "build.Dockerfile")
    io.write(buildfile, outputfolder + "build.sh")


    print("Running Stage 2")
    earthfile = gha_to_bash_prompt.prompt2(file_structure, runfile,dockerfile, buildfile)
    io.write(earthfile, outputfolder + "Earthfile")

if __name__ == '__main__':
    main()