from typing import List, Optional
from pprint import pprint
from pprint import pprint
from textwrap import dedent
from core.io import read
import time

from core.io import call_chat_completion_api_cached, call_chat_completion_api

import os

def initialize_examples(path: str):
    input_files = []
    output_files = []

    for file in os.listdir(path):
        if file.startswith("in"):
            input_files.append(os.path.join(path, file))
        elif file.startswith("out"):
            output_files.append(os.path.join(path, file))

    input_files.sort()
    output_files.sort()

    return [(read(input_file), read(output_file)) for input_file, output_file in zip(input_files, output_files)]

summarize_tests = initialize_examples("data/summary_fewshot")
dockerfile_tests = initialize_examples("data/docker_fewshot")

def summarize_gha(s : str) -> str:
    messages=[]
    messages = [{"role": "system", "content": dedent(f"""
        Given a GitHub Actions workflow YAML file, summarize how you would recreate the steps of this build in a bash file. 
        List preconditions like "install python 3.11" before steps requiring them.
        Skip things that aren't revelevant to porting it to a bash script or makefile.
        Skip git cloning, and changing into the repo.
        Skip prereqs: docker and git.
        Be concise.
        """)}]
    
    for test_input, test_output in summarize_tests:
        messages.extend([
            {"role": "user", "content": test_input},
            {"role": "assistant", "content": test_output},
        ])
    
    messages.append({"role": "user", "content": s})
    return call_chat_completion_api_cached(
    temperature=0.1, 
    max_tokens=300,
    messages = messages)

dockerfile_tests = [
    (read("data/docker_fewshot/in1.md"),read("data/docker_fewshot/out1.Dockerfile"))
]
# The Dockerfile format here is sort of part way between Earthly and Docker.
def create_dockerfile(file_structure : str, build_script: str, existing_dockerfile: str) -> str:
    image_list = read("data/images.txt")
    messages=[]
    messages = [{"role": "system", "content": dedent(f"""
        You are creating a multi-stage dockerfile based on three inputs. 
        1) A list of images, that you use to help select the base image to use in your dockerfile. 
        2) A Description of the file structure of the project. Use the file structure to determine what files need to be copied in at each stage of the docker multi-stage build. 
        3) A list of steps to be performed each in a seperate stage of the dockerfile, given as an ordered markdown list of statments to be RUN inside each stage.
        4) Optionally an existing dockerfile
        The Dockerfile format has additional features like `SAVE IMAGE`
        Be concise and return only the contents of the dockerfile, wihtout backticks.
        """)}]
    
    for test_input, test_output in dockerfile_tests:
        messages.extend([
            {"role": "user", "content": test_input},
            {"role": "assistant", "content": test_output},
        ])
    
    messages.append({"role": "user", "content": f"""
        ## Images
        ```
        {dedent(image_list)}
        ```

        ## Files
        ```
        {dedent(file_structure)}
        ```

        ## Build Steps
        ```
       {dedent(build_script)} 
        ```

        ## Existing Dockerfile
        ```
       {dedent(existing_dockerfile)} 
        ```
    """})
    generated = call_chat_completion_api_cached(
    temperature=0.1, 
    max_tokens=1000,
    messages = messages)
    return generated 

earthfile_tests = initialize_examples("data/earthly_fewshot")

earthly_basics = read("data/earthly_docs/basics.md") 
earthly_reference = read("data/earthly_docs/summary.md") 

def create_earthfile(dockerfile : str) -> str:
    messages=[]
    messages = [{"role": "system", "content": dedent(f"""
        Use the below documentation on Earthfiles to do a code conversion task.
        Article:
        \"\"\"
        {earthly_basics} 
        {earthly_reference} 
        \"\"\"

        Conversion Task:
        You are converting a multistage Dockerfile to an Earthly Earthfile.
        Copy in the files needed just before they are used.
        Be concise and return only the contents of the Earthfile, without backticks.
        Make sure to use the Earthfile format for `COPY` and `SAVE ARTIFACT`
        """)}]
    
    for test_input, test_output in earthfile_tests:
        messages.extend([
            {"role": "user", "content": test_input},
            {"role": "assistant", "content": test_output},
        ])
    
    messages.append({"role": "user", "content": dockerfile})
    pprint(messages)
    return call_chat_completion_api_cached(
    temperature=0.0, 
    max_tokens=1000,
    messages = messages)

earthfilefix_tests = initialize_examples("data/earthlyfix_fewshot")

def fix_earthfile(earthfile : str) -> str:
    messages=[]
    messages = [{"role": "system", "content": dedent(f"""
        Use the below documentation on Earthfiles for this task.
        Article:
        \"\"\"
        {earthly_basics} 
        {earthly_reference} 
        \"\"\"

        Task:
        You are given an Earthfile that has incorrect syntax or doesn't conform to best practices.
        It may user Dockerfile syntax, or not SAVE ARTIFACT for things it COPY or there just may be a better way to structure things.
        Return a corrected Earthfile. If no mistakes are found, return it as is.
        Be concise and return only the contents of the Earthfile, without backticks. 
        """)}]
    
    for test_input, test_output in earthfilefix_tests:
        messages.extend([
            {"role": "user", "content": test_input},
            {"role": "assistant", "content": test_output},
        ])
    
    messages.append({"role": "user", "content": earthfile})
    pprint(messages)
    return call_chat_completion_api_cached(
    temperature=0.0, 
    max_tokens=1000,
    messages = messages)