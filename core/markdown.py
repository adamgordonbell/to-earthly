from typing import List
import re
import mistune

# class CodeBlockRenderer(mistune.Renderer):
#     def __init__(self):
#         super(CodeBlockRenderer, self).__init__()
#         self.code_blocks = []

#     def block_code(self, code, lang=None):
#         self.code_blocks.append(code)
#         return ''  # return an empty string, we are only interested in extracting code blocks

# def extract_code_blocks(markdown: str) -> List[str]:
#     # Add an extra line with three backticks before each filename
#     markdown = re.sub(r'\n`', '\n```\n`', markdown)

#     renderer = CodeBlockRenderer()
#     mistune_markdown = mistune.Markdown(renderer=renderer)
#     mistune_markdown(markdown)
#     return renderer.code_blocks

def extract_code_blocks(markdown: str) -> List[str]:
    print(markdown)
    in_code_block = False
    code_blocks = []
    current_block = []

    lines = markdown.split('\n')
    for line in lines:
        if line.strip().startswith('```'):
            if in_code_block:  # End of a block
                code_blocks.append('\n'.join(current_block))
                current_block = []
            in_code_block = not in_code_block
        elif in_code_block:  # Inside a block
            current_block.append(line)

    return code_blocks