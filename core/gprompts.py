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

dotenv.load_dotenv()
gpt4 = guidance.llms.OpenAI("gpt-4")

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
   
    
    # for test_input, test_output in summarize_tests:
    #     messages.extend([
    #         {"role": "user", "content": test_input},
    #         {"role": "assistant", "content": test_output},
    #     ])
    
    # messages.append({"role": "user", "content": s})
    identify = guidance(dedent('''
        {{#system~}}
        Given a GitHub Actions workflow YAML file, summarize how you would recreate the steps of this build in a bash file. 
        List preconditions like "install python 3.11" before steps requiring them.
        Skip things that aren't revelevant to porting it to a bash script or makefile.
        Skip git cloning, and changing into the repo and docker login.
        Skip prereqs: docker and git.
        Don't answer the question yet. Instead discuss what steps should be included and which shouldn't be.
        {{~/system}}
        {{#user~}}
        {{input}}
        {{~/user}}
        {{#assistant~}}
        {{gen "discuss" temperature=0 max_tokens=2000}}
        {{~/assistant}}  
        {{#user~}}
        Great, now summarize how you would recreate the steps of this build in a bash file.
        {{~/user}}
        {{#assistant~}}
        {{gen "summary" temperature=0 max_tokens=2000}}
        {{~/assistant}}  
    '''), llm=gpt4)
    out = identify(input=dedent(s))
    pprint(out)
    return out["summary"]

