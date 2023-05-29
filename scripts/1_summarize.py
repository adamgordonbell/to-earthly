from typing import List, Optional, Callable
from pprint import pprint

# from core.io import write_sections
from core import io, prompts

inputfolder: str = 'test_cases/node_server/input'
outputfolder: str = 'test_cases/node_server/output'

outputfile: str = f'{outputfolder}/summary.md'

def main() -> None:
    yml = io.find_first_yml(inputfolder)
    summarize : str = prompts.summarize_gha(yml)
    io.write(summarize, outputfile)

if __name__ == '__main__':
    main()