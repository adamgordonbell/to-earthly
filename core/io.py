from typing import Callable, List, Optional
from pprint import pprint
from pprint import pprint
from textwrap import dedent
from joblib import Memory
from dotenv import load_dotenv
from collections import defaultdict
import openai
import time
import os
import subprocess
import glob
import core.boot

memory = Memory(location='data/gpt_cache', verbose=1)

openai.api_key = os.getenv('OPENAI_API_KEY')

# @memory.cache
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

def relative_read(relative_filepath: str) -> str:
    # Get the directory of the current script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full filepath, by going up one folder
    full_filepath = os.path.join(script_dir, ".." ,relative_filepath)

    with open(full_filepath, 'r') as outfile:
        return outfile.read()

def write(contents: str, filepath: str) -> None:
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filepath, 'w') as outfile:
        outfile.write(contents)

def find_first_yml(path=None) -> str:
    if path is None:
        path = os.getcwd()
        
    if not path.endswith("/"):
        path += "/"

    yml_files = glob.glob(path + ".github/workflows/*.yml")

    if not yml_files:
        raise Exception("No yml files found. Process will stop.")

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

# Like tree but less output
def print_directory(path, prefix='', level=0, max_level=1) -> str:
    if level > max_level:
        return ''

    dir_structure = ''
    dir_items = defaultdict(list)

    # Group files by extension and directories separately
    for item in os.listdir(path):
        # Ignore hidden files and directories
        if item.startswith('.'):
            continue

        if os.path.isfile(os.path.join(path, item)):
            ext = os.path.splitext(item)[1]
            dir_items[ext].append(item)
        else:
            dir_items['folders'].append(item)

    # Generate directory structure, combining files with same extension if more than 3
    for ext, items in dir_items.items():
        if ext != 'folders':
            if len(items) > 3:
                dir_structure += f"{prefix}├── *{ext}\n"
            else:
                for item in items:
                    dir_structure += f"{prefix}├── {item}\n"
        else:
            for item in items:
                dir_structure += f"{prefix}├── {item}/\n"
                if level < max_level:
                    subdir_structure = print_directory(os.path.join(path, item), prefix + "│   ", level + 1, max_level)
                    dir_structure += subdir_structure

    return dir_structure
