from unittest import result

from services.gemnnii_service import generate_response
from tools.file_tools import write_file
def generate_code_node(state):
    print("generating code for task")
    prompt = f"""
    You are a helpful assistant that generates code based on the given task. 
    The task is: {state['task']}
    No explainations and no markdown, just the code. 
    
    Implementation Plan:
    {state['plan']} 
    """
    code = "".join(
        generate_response(prompt)
    )
    state['generated_code'] = code
    return state

def review_code_node(state):
    print("currently reviewing the code")
    prompt = f"""
        You are a senior and Experienced code reviewer.
        Review the following code.
        If the code is correct, respond with exactly:
        APPROVED
        If the code contains bugs or serious issues, respond with exactly:
        NEEDS_FIX
        Code:
        {state['generated_code']}
        """
    result = "".join(
        generate_response(prompt)
    )
    state['reviewed_result'] = result
    return state

def route_after_review_node(state):
   if "APPROVED" in state['reviewed_result']:
      return "save_code"
   return "fix_code"

def fix_code_node(state):
    print("currently fixing the code")

    prompt = f"""
    You are a senior coding engineer.
    Fix any bugs in this code.
    Return ONLY the corrected code.
    Code:
    {state['generated_code']}
    """
    fixed_code = "".join(
        generate_response(prompt)
    )

    state["reviewed_code"] = fixed_code

    return state

def planner_node(state):
    print("Planning the next steps")
    prompt = f"""
    You are a senior software architect.
    Create a concise implementation plan for the following task.
    Task:
    {state['task']}
    Return only the plan.
    No markdown.
    No code.
    """
    plan = "".join(
        generate_response(prompt)
    )
    state['plan'] = plan
    return state

def save_code_node(state):
    print("saving the code to a file")
    file_path = write_file(state['filename'], state['generated_code'])
    state['file_path'] = file_path
    return state

