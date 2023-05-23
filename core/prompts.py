from typing import List, Optional
from pprint import pprint
from pprint import pprint
from textwrap import dedent
from core.io import read
import time

from core.io import call_chat_completion_api_cached, call_chat_completion_api

summarize_tests = [
    (read("data/summary_fewshot/in1.yaml"),read("data/summary_fewshot/out1.md")),
    (read("data/summary_fewshot/in2.yaml"),read("data/summary_fewshot/out2.md"))
]

def summarize_gha(s : str) -> str:
    messages=[]
    messages=[
        {"role": "system", "content": dedent(f"""
            Given a GitHub Actions workflow YAML file, summarize how you would recreate the steps of this build in a bash file. 
            List preconditions like "install python 3.11" before steps requiring them.
            Skip things that aren't revelevant to porting it to a bash script or makefile.
            Skip git cloning, and changing into the repo.
            Skip prereqs: docker and git.
            Be concise.
            """)},
        {"role": "user", "content": summarize_tests[0][0]},
        {"role": "assistant", "content": summarize_tests[0][1]},
        {"role": "user", "content": summarize_tests[1][0]},
        {"role": "assistant", "content": summarize_tests[1][1]},
        {"role": "user", "content": s},
        ]
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
    messages=[
        {"role": "system", "content": dedent(f"""
                                                 You are creating a multi-stage dockerfile based on three inputs. 
                                                 1) A list of images, that you use to help select the base image to use in your dockerfile. 
                                                 2) A Description of the file structure of the project. Use the file structure to determine what files need to be copied in at each stage of the docker multi-stage build. 
                                                 3) A list of steps to be performed each in a seperate stage of the dockerfile, given as an ordered markdown list of statments to be RUN inside each stage.
                                                 4) Optionally an existing dockerfile
                                                 The Dockerfile format has additional features like `SAVE IMAGE`
                                                 Be concise and return only the contents of the dockerfile, wihtout backticks.""")},
        {"role": "user", "content": dockerfile_tests[0][0]},
        {"role": "assistant", "content": dockerfile_tests[0][1]},
        {"role": "user", "content": f"""
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
        """},
        ]
    generated = call_chat_completion_api_cached(
    temperature=0.1, 
    max_tokens=1000,
    messages = messages)
    return generated 

earthfile_tests = [
    (read("data/earthly_fewshot/in1.md"),read("data/earthly_fewshot/out1.md")),
    (read("data/earthly_fewshot/in2.md"),read("data/earthly_fewshot/out2.md")),
]

earthly_basics = read("data/earthly_docs/basics.md") 

def create_earthfile(dockerfile : str) -> str:
    messages=[]
    messages=[
        {"role": "system", "content": dedent(f"""
            You are converting a multistage Dockerfile to an Earthly Earthfile.
            Copy in the files needed just before they are used.
            Be concise and return only the contents of the Earthfile, without backticks.

            Here's a basic tutorial on Earthly's Earthfiles:
            {earthly_basics} 
            """)},
        {"role": "user", "content": earthfile_tests[0][0]},
        {"role": "assistant", "content": earthfile_tests[0][1]},
        {"role": "user", "content": earthfile_tests[1][0]},
        {"role": "assistant", "content": earthfile_tests[1][1]},
        {"role": "user", "content": dockerfile},
        ]
    pprint(messages)
    return call_chat_completion_api_cached(
    temperature=0.1, 
    max_tokens=1000,
    messages = messages)