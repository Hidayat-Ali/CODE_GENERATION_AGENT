from langgraph.graph import END

from services.gemnnii_service import generate_response
from tools.file_tools import write_file,read_file
def generate_code_node(state):
    print("generating code for task")
    prompt = f"""
    You are a helpful assistant that generates code based on the given task. 
    The task is: {state['task']}
    No explainations and no markdown, just the code. 
    
    Implementation Plan:
    {state['plan']} 
    """
    # code = "".join(
    #     generate_response(prompt)
    # )
    state['generated_code'] = f"# This is the generated code for {state['current_file']} based on the task: {state['task']}\n\n"
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
    # result = "".join(
    #     generate_response(prompt)
    # )
    state['reviewed_result'] = "APPROVED"
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

    print("Planning project")

    plan_prompt = f"""
    Create an implementation plan.

    Task:
    {state['task']}
    """

    file_prompt = f"""
    You are a senior software architect.

    Task:
    {state['task']}

    Return only filenames.

    One filename per line.

    Example:

    main.py
    models.py
    database.py
    """

    # plan = "".join(
    #     generate_response(plan_prompt)
    # )

    # files_text = "".join(
    #     generate_response(file_prompt)
    # )
    plan = """
1. Create main.py
2. Create models.py
3. Create routes.py
"""

    state["plan"] = plan

    # state["files"] = [
    #     line.strip()
    #     for line in files_text.splitlines()
    #     if line.strip()
    # ]
    state["files"] = [
        "main.py",
        "database.py",
        "models.py",
        "routes.py"
    ]

    state['current_file_index'] = 0
    state['current_file'] = state['files'][state['current_file_index']]

    return state

def next_file_node(state):
    state['current_file_index'] += 1
    state['current_file'] = state['files'][state['current_file_index']]
    return state

def save_code_node(state):
    print("saving the code to a file")

    file_path = write_file(
        state["current_file"],
        state["generated_code"]
    )

    state["file_path"] = file_path

    if "generated_files" not in state:
        state["generated_files"] = []

    state["generated_files"].append(
        state["current_file"]
    )

    return state

def route_after_saving_node(state):
    if state['current_file_index'] < len(state['files']) - 1:
        return "next_file"
    return END

def collect_context_node(state):
    print(f"collecting context from generated files {state['generated_files']}")
    context = ""

    for file in state["generated_files"]:

        content = read_file(file)

        context += f"""
        FILE: {file}

        {content}

        """

    state["project_context"] = context
    print(state['project_context'])

    return state