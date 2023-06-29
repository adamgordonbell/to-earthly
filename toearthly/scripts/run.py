from textwrap import dedent
import argparse

from toearthly.core import io, gha_to_bash_prompt

# Default directories
DEFAULT_INPUT_DIR = '/input/'
DEFAULT_EARTHFILE_PATH = '/input/Earthfile'
DEFAULT_DEBUG_DIR = '/input/.to_earthly/'


intro = """
ALPHA ALERT
This program attempts to generate an Earthfile using an Existing GitHub actions 
workflow.
The generated Earthfile should be a good starting place. Additional manual changes 
may be needed.
This program will send your GitHub actions workflow to OpenAPI.

This program assumes your project has the following attributes:
 * Primarily a single programming language
 * Not a deeply nested monorepo

Please send any stange results or issues to adam@earthly.dev along with a copy of the
.to_earthly folder and the Earthfile. I will use this for future improvements. 

Many things need to be supported and will be ignored for now. These include:
* container creation
* matrix builds
* WITH DOCKER and integration tests
* Github workflow can not be specified. 
(picks first result from .github/workflows/*.yml )

I'll prioritize these based on feedback. So reach out on slack or via adam@earthly.dev
or via https://github.com/adamgordonbell/to-earthly
"""

debug_dir = None

def main(input_dir: str, earthfile_path : str, debug_dir_arg: str) -> None:
    global debug_dir
    debug_dir = debug_dir_arg
    print(intro)
    input("Press Enter to continue...")
    yml,path = io.find_first_yml(input_dir)
    print(dedent(f"""
          Input:
          Workflow:\t{path}
          Output:\t\t{earthfile_path}
          Debug files:\t{debug_dir}
          """))
    file_structure = io.print_directory(input_dir)
    extra_docker_file = io.find_first_dockerfile(input_dir)
    debug_io = DebugIO(debug_dir)
    debug_io.write(yml, "workflow.yml")
    debug_io.write(file_structure, "files.txt")
    debug_io.write(extra_docker_file, "Dockerfile")

    print("Starting...\n (This may take 10 minutes)")
    print("Running Stage 1")
    runfile, dockerfile, buildfile = gha_to_bash_prompt.prompt1(yml, file_structure, debug_dir)

    print("Running Stage 2")
    gha_to_bash_prompt.prompt2(
        file_structure, 
        runfile,
        dockerfile, 
        buildfile,
        debug_dir)

    print("Running Stage 3")
    earthfile = gha_to_bash_prompt.prompt3(earthfile, yml, file_structure, debug_dir)
    io.write(earthfile, earthfile_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="Base file location", 
                        default=DEFAULT_INPUT_DIR)
    parser.add_argument("--earthfile", help="Earthfile path", 
                        default=DEFAULT_EARTHFILE_PATH)
    parser.add_argument("--debug_dir", help="Debug directory location", 
                        default=DEFAULT_DEBUG_DIR)
    args = parser.parse_args()

    main(args.input_dir, args.earthfile, args.debug_dir)