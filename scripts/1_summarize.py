from typing import List, Optional, Callable
from pprint import pprint

# from core.io import write_sections
from core.prompts import summarize_gha
from core.io import write, find_first_yml

inputfolder: str = 'test_cases/node_server/input'
outputfolder: str = 'test_cases/node_server/output'

outputfile: str = f'{outputfolder}/summary.md'

def main() -> None:
    yml = find_first_yml(inputfolder)
    summarize : str = summarize_gha(yml)
    write(summarize, outputfile)

if __name__ == '__main__':
    main()