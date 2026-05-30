from services.gemnnii_service import generate_response
from tools.file_tools import write_file
def generate_code_node(state):
    prompt = f"""
    You are a helpful assistant that generates code based on the given task. 
    The task is: {state['task']}
    No explainations and no markdown, just the code. 
    """
    code = "".join(
        generate_response(prompt)
    )
    state['generated_code'] = code
    return state

def review_code_node(state):
    prompt = f"""
    You are experenced software engineer that reviews code and fixes the bug if found in the code. 
    The generated code is: {state['generated_code']}
    fix the code if you find any bug, otherwise return the same code.
    No explainations and no markdown, just the code.
    """
    code = "".join(
        generate_response(prompt)
    )
    state['reviewed_code'] = code
    return state


def save_code_node(state):
    file_path = write_file(state['filename'], state['generated_code'])
    state['file_path'] = file_path
    return state

