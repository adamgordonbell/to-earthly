from typing import Callable, List, Optional
from pprint import pprint
from pprint import pprint
from textwrap import dedent
from joblib import Memory
from dotenv import load_dotenv
import openai
import time
import os
import subprocess
import glob

memory = Memory(location='data/gpt_cache', verbose=1)

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

@memory.cache
def call_chat_completion_api_cached(max_tokens, messages,temperature):
    print("running prompt")
    return call_chat_completion_api(max_tokens,messages, temperature)


def call_chat_completion_api(max_tokens, messages,temperature):
    max_retries = 3
    initial_delay = 1
    factor = 2

    retries = 0
    delay = initial_delay

    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}, Retrying...")
            time.sleep(delay)
            retries += 1
            delay *= factor
    print("Max retries reached. Returning 'Error'.")
    return "Error: Max Retry Hit"

def read(filepath: str) -> str:
    with open(filepath, 'r') as outfile:
        return outfile.read()

def write(contents: str, filepath: str) -> None:
    with open(filepath, 'w') as outfile:
        outfile.write(contents)

def find_first_yml(path=None) -> str:
    if path is None:
        path = os.getcwd()
        
    if not path.endswith("/"):
        path += "/"

    yml_files = glob.glob(path + ".github/workflows/*.yml")

    if not yml_files:
        raise Exception("No yml files found.")

    with open(yml_files[0], 'r') as file:
        return file.read()
    

def find_first_dockerfile(path=None) -> str:
    if path is None:
        path = os.getcwd()
        
    if not path.endswith("/"):
        path += "/"

    docker_files = glob.glob(path + "Dockerfile")

    if not docker_files:
        return ""

    with open(docker_files[0], 'r') as file:
        return file.read()


def run_tree(path=None, level=2) -> str:
    initial_directory = os.getcwd()
    if path is None:
        path = initial_directory

    os.chdir(path)
    result = subprocess.run(["tree", "-F", "-L", str(level), "--noreport", '.'], capture_output=True, text=True)
    os.chdir(initial_directory)

    if result.returncode != 0:
        raise Exception(f"Failed to run tree command: {result.stderr}")

    return result.stdout