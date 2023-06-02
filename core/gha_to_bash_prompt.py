from typing import List, Optional
from pprint import pprint
from pprint import pprint
from textwrap import dedent
from core.io import read
import time
import dotenv 

from core import io
import os
import guidance
from typing import Tuple

dotenv.load_dotenv()
gpt4 = guidance.llms.OpenAI("gpt-4")

import re

def extract_code_blocks(markdown : str) -> List[str]:
    # This regex pattern matches code blocks in markdown
    pattern = r"```(.*?)```"

    # This finds all code blocks in the markdown string
    matches = re.findall(pattern, markdown, re.DOTALL)

    # This removes the language specification from the code block
    matches = [re.sub(r'^[a-zA-Z]*\n', '', match) for match in matches]

    return matches

input1 = io.read("test_cases/python_lint/training/workflow.yml")
cot1 = io.read("test_cases/python_lint/training/gha_to_bash_prompt_plan.md")
result1 = io.read("test_cases/python_lint/training/gha_to_bash_prompt_result.md")

def prompt1(s : str) -> Tuple[str, str, str, str, str]:
 
    identify = guidance(dedent('''
        {{#system~}}
        Given a GitHub Actions workflow YAML file, summarize how you would recreate the steps of this build using bash and docker.

        The implementation will consist of a run.sh script that creates and runs a Docker container where our build.sh script is executed. This approach encapsulates our build process in a controlled environment (the Docker container), isolating it from the host machine and ensuring that it has all the necessary dependencies, regardless of where or on what machine the build is running. This is why we choose to use Docker and why we run the build process inside a Docker container, even though it may seem like overkill for  some simple build processes.

        You will create three files:
        * `run.sh`: A bash file that wraps docker. It will call docker build and afterward run steps like docker push. Steps like git cloning and changing into the repo aren't needed because this file is stored in the git repository along with the code.
        * `build.Dockerfile`: A dockerfile with the correct base image to support the build steps. This includes any programming language tool and any dependencies needed for `build.sh`. 
        * `build.sh` A bash file that runs the steps of the build process. It will run inside `build.Dockerfile` in the working directory of the repository. 

        Other files will exist in the repository. Code files and other assets and possibly an application Dockerfile. Call that `app`.

        Important considerations:
        * no need to install dependencies, nor check out the code in `build.sh`because it is run inside the image produced from `build.Dockerfile`. Call that docker image `build`.
        * `build.Dockerfile` should work without volume mounting. Files that are needed need to be copied in. 
        * References to building/tagging and pushing a Docker image or container in GitHub Actions workflow YAML do not refer to `build.Dockerfile` and `build` but to the application `app` Dockerfile called `Dockerfile`. 
        * Any pushing and tagging of images should be of images made from  app `Dockerfile` and not from `build.Dockerfile`. Docker image `build` is used strictly for building steps and is used as a way to set up dependencies for that build in a repeatable way. 
        * Don't include any steps that executing the git hub action wouldn't produce. This may mean a step does nothing. 
        * You do not need to mention chmod of `build.sh` or `run.sh`. That is taken care of.

        Do not produce the files. Instead, describe how you would approach this problem. Then go through the yaml document section by section and discuss if steps should be included or omitted, which of the three files it should be in, and how it needs to be adapted to the new format.
        {{~/system}}

        {{#user~}}
        {input1}
        {{~/user}} 
        {{#assistant~}}
        {{cot1}}
        {{~/assistant}}
        {{#user~}}
        Ok, produce `run.sh`,`build.Dockerfile` and `build.sh`. Remember`build.Dockerfile` should work without volume mounting: files that are needed need to be copied in.
        {{~/user}}
        {{#assistant~}}
        {{result1}}
        {{~/assistant}}
        {{#user~}}
        {{input}}
        {{~/user}}
        {{#assistant~}}
        {{gen "discuss" temperature=0 max_tokens=2000}}
        {{~/assistant}}
        {{#user~}}
        Ok, produce `run.sh`,`build.Dockerfile` and `build.sh`. Remember`build.Dockerfile` should work without volume mounting: files that are needed need to be copied in. 
        {{~/user}}
        {{#assistant~}}
        {{gen "files" temperature=0 max_tokens=500}}
        {{~/assistant}}

    '''), llm=gpt4)
    out = identify(input=dedent(s), input1=input1, cot1=cot1, result1=result1)
    results = extract_code_blocks(out["files"])
    if len(results) != 3:
        raise ValueError(f"3 Files exepected back. Instead got {len(results)}")
    return (out["discuss"],out["files"], results[0], results[1], results[2])

earthly_basics = read("data/earthly_docs/basics.md") 
input1 = io.read("test_cases/python_lint/training/files.md")
cot1 = io.read("test_cases/python_lint/training/EarthfilePlan.md")
result1 = io.read("test_cases/python_lint/training/Earthfile")

def prompt2(files: str, run : str, docker : str, build : str) ->  Tuple[str,str]:
    identify = guidance(dedent('''
        {{#system~}}
        You are creating an Earthfile from several bash and dockerfiles. I'll share Earthly documentation with you and then describe the conversion process. 

        {{tutorial}}
        The tutorial is over. I will now describe the task.

        You are creating an Earthfile from the following inputs. 
        *  `Files`: A Description of the file structure of the project. Use the file structure to determine what files need to be copied in at each stage of the docker multi-stage build. 
        * `run.sh`: A bash file that wraps docker. It will call docker build and afterward run steps like docker push. 
        * `build.Dockerfile`: A dockerfile with the correct base image to support the build steps. This should become the `base` and possibly the `deps` steps in the docker file.
        * `build.sh` A bash file that runs the build steps. These steps should become targets in the Earthfile. 
        {{~/system}}
        {{#user~}}
        {input1}
        {{~/user}} 
        {{#assistant~}}
        {{cot1}}
        {{~/assistant}}
        {{#user~}}
        Ok, produce the files. Files that are needed need to be copied in. 
        {{~/user}}
        {{#assistant~}}
        {{result1}}
        {{~/assistant}}
        {{#user~}}
        `Files:`
        ```
        {{files}}
        ```

        `run.sh`:
        ```
        {{run}}
        ```

        build.Dockerfile
        ```
        {{docker}}
        ```

        `build.sh`:
        ```
        {{build}}
        ```

        An Earthfile is a better way to represent this build process because it combines the concepts of running bash commands to build something with the ideas of containerisation made popular by Docker and dockerfile.

        Task:
        Do not produce the Earthfile. Instead,  describe how you would approach this problem. Then go through the files, step by step, and discuss how the steps should be ported to Earthly. 
        {{~/user}}
        {{#assistant~}}
        {{gen "discuss" temperature=0 max_tokens=2000}}
        {{~/assistant}}
        {{#user~}}
        Ok, produce the files. Files that are needed need to be copied in. 
        {{~/user}}
        {{#assistant~}}
        {{gen "Earthfile" temperature=0 max_tokens=2000}}
        {{~/assistant}}

    '''), llm=gpt4)
    out = identify(tutorial="earthly_basics", input1=input1, cot1=cot1, result1=result1, files=files, run=run,docker=docker, build=build)
    results = extract_code_blocks(out["Earthfile"])

    # if len(results) != 1:
        # raise ValueError(f"1 Files exepected back. Instead got {len(results)}")
    return (out["discuss"],results[0])

