from typing import List, Optional, Callable
from pprint import pprint

from core import io, prompts, gprompts

inputfolder: str = 'test_cases/node_server/input'
outputfolder: str = 'test_cases/node_server/output'

outputfile: str = f'{outputfolder}/gsummary.md'

def main() -> None:
    yml = io.find_first_yml(inputfolder)
    summarize : str = gprompts.summarize_gha(yml)
    io.write(summarize, outputfile)

if __name__ == '__main__':
    main()