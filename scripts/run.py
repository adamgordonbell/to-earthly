from typing import List, Optional, Callable
from pprint import pprint
from textwrap import dedent
import argparse

from core import io, gha_to_bash_prompt

# Default directories
DEFAULT_INPUT_DIR = '/input/'
DEFAULT_EARTHFILE_PATH = '/input/Earthfile'
DEFAULT_OUTPUT_DIR = '/input/.to_earthly/'


def main(input_dir: str, earthfile_path : str, output_dir: str) -> None:
    print("Gathering Data")
    yml = io.find_first_yml(input_dir)
    # file_structure = io.run_tree(input_dir)
    file_structure = io.print_directory(input_dir)
    extra_docker_file = io.find_first_dockerfile(input_dir)
    io.write(yml,output_dir + "workflow.yml")
    io.write(file_structure,output_dir + "files.txt")
    io.write(extra_docker_file,output_dir + "Dockerfile")

    print("Running Stage 1")
    discuss1, result, runfile, dockerfile, buildfile = gha_to_bash_prompt.prompt1(yml, file_structure)
    io.write(discuss1, output_dir + "gha_to_bash_prompt_plan.md")
    io.write(result, output_dir + "gha_to_bash_prompt_result.md")
    io.write(runfile, output_dir + "run.sh")
    io.write(dockerfile, output_dir + "build.Dockerfile")
    io.write(buildfile, output_dir + "build.sh")

    print("Running Stage 2")
    discuss, earthfile = gha_to_bash_prompt.prompt2(file_structure, runfile,dockerfile, buildfile)
    io.write(discuss, output_dir + "EarthfilePlan.md")
    io.write(earthfile, output_dir + "Earthfile.1")

    print("Running Stage 3")
    discuss, earthfile = gha_to_bash_prompt.prompt3(earthfile, yml, file_structure)
    io.write(discuss, output_dir + "EarthfileFixPlan.md")
    io.write(earthfile, earthfile_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="Base file location", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--earthfile", help="Earthfile path", default=DEFAULT_EARTHFILE_PATH)
    parser.add_argument("--output_dir", help="Output directory location", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    main(args.input_dir, args.earthfile, args.output_dir)