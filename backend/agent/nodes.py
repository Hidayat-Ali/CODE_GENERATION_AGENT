from langgraph.graph import END
import subprocess
from pathlib import Path

# from services.gemnnii_service import generate_response

from tools.file_tools import write_file, read_file


def generate_code_node(state):
    state.pop("reviewed_code", None)
    print("generating code for task")

    # prompt = f"""
    # You are a helpful assistant that generates code based on the given task.
    # The task is: {state['task']}
    # No explainations and no markdown, just the code.
    #
    # Implementation Plan:
    # {state['plan']}
    # """
    #
    # code = "".join(
    #     generate_response(prompt)
    # )


    if state["current_file"] == "requirements.txt":
        state["generated_code"] = """
    uvicorn
    fastapi
    sqlalchemy
    psycopg2-binary
    python-dotenv
    """
        return  state

    state["generated_code"] = """
    print(x)
    print(c)
    """

    return state


def review_code_node(state):
    print("currently reviewing the code")

    # prompt = f"""
    # You are a senior and Experienced code reviewer.
    # Review the following code.
    # If the code is correct, respond with exactly:
    # APPROVED
    # If the code contains bugs or serious issues, respond with exactly:
    # NEEDS_FIX
    # Code:
    # {state['generated_code']}
    # """
    #
    # result = "".join(
    #     generate_response(prompt)
    # )

    state["reviewed_result"] = "APPROVED"

    return state


def route_after_review_node(state):
    if "APPROVED" in state["reviewed_result"]:
        return "save_code"

    return "fix_code"


def fix_code_node(state):
    print("currently fixing the code")

    # prompt = f"""
    # You are a senior coding engineer.
    # Fix any bugs in this code.
    # Return ONLY the corrected code.
    # Code:
    # {state['generated_code']}
    # """
    #
    # fixed_code = "".join(
    #     generate_response(prompt)
    # )
    if state["current_file"] == "requirements.txt":
        state["reviewed_code"] = "uvicorn fastapi sqlalchemy psycopg2-binary python-dotenv"
    else:
        state["reviewed_code"] = """print("Fixed code executed")"""
    state['retry_count'] = (
        state.get("retry_count", 0) + 1
    )

    return state


def planner_node(state):

    print("Planning project")

    # plan_prompt = f"""
    # Create an implementation plan.
    #
    # Task:
    # {state['task']}
    # """
    #
    # file_prompt = f"""
    # You are a senior software architect.
    #
    # Task:
    # {state['task']}
    #
    # Return only filenames.
    #
    # One filename per line.
    #
    # Example:
    #
    # main.py
    # models.py
    # database.py
    # """
    #
    # plan = "".join(
    #     generate_response(plan_prompt)
    # )
    #
    # files_text = "".join(
    #     generate_response(file_prompt)
    # )

    plan = """
1. Create main.py
2. Create database.py
3. Create models.py
4. Create routes.py
"""

    files_text = """
main.py
database.py
models.py
routes.py
requirements.txt
"""

    state["plan"] = plan

    state["files"] = [
        line.strip()
        for line in files_text.splitlines()
        if line.strip()
    ]

    state["current_file_index"] = 0
    state["current_file"] = state["files"][0]

    return state


def next_file_node(state):
    state["retry_count"] = 0
    state["current_file_index"] += 1
    state["current_file"] = state["files"][state["current_file_index"]]
    return state


def save_code_node(state):
    print("saving the code to a file")
    print("CURRENT FILE:", state["current_file"])
    print("GENERATED CODE:", state.get("generated_code"))
    print("REVIEWED CODE:", state.get("reviewed_code"))

    if state["current_file"] == "requirements.txt":
        code_to_save = state["generated_code"]
    else:
        code_to_save = state.get(
            "reviewed_code",
            state["generated_code"]
        )

    file_path = write_file(
        state["current_file"],
        code_to_save
    )

    state["file_path"] = file_path

    if "generated_files" not in state:
        state["generated_files"] = []

    if "generated_files" not in state:
        state["generated_files"] = []

    if state["current_file"] not in state["generated_files"]:
        state["generated_files"].append(
        state["current_file"]
    )

    return state


def route_after_saving_node(state):
    if state["current_file_index"] < len(state["files"]) - 1:
        return "next_file"

    return END


def collect_context_node(state):
    print(
        f"collecting context from generated files {state['generated_files']}"
    )

    context = ""

    for file in state["generated_files"]:

        content = read_file(file)

        context += f"""
FILE: {file}

{content}

"""

    state["project_context"] = context

    print(state["project_context"])

    return state


def execute_code_node(state):
    print(
        f"Exectuting the {state['current_file']} in docker"
    )

    # Skip execution for non-python files
    if not state["current_file"].endswith(".py"):
        print(
            f"Skipping execution of {state['current_file']}"
        )

        state["execution_result"] = ""
        state["execution_error"] = ""
        state["execution_success"] = True

        return state

    workspace_path = (
        Path.cwd() / "workspace/generated"
    ).resolve()

    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{workspace_path}:/app",
            "python:3.11",
            "python",
            f"/app/{state['current_file']}"
        ],
        capture_output=True,
        text=True
    )

    state["execution_result"] = result.stdout
    state["execution_error"] = result.stderr
    state["execution_success"] = (
        result.returncode == 0
    )

    print("OUTPUT:\n")
    print(result.stdout)

    print("ERROR:\n")
    print(result.stderr)

    return state


def dependency_error_node(state):
    print("Dependency error detected")
    print(state["execution_error"])
    return state


def route_after_execution_node(state):

    if state["execution_success"]:
        return "collect_context"

    if is_dependency_error(state["execution_error"]):
        return "dependency_error"
    if state.get("retry_count", 0) >= 3:
        print("Maximum retry count reached")
        return "dependency_error"
    

    return "fix_code"


def is_dependency_error(error):
    return "ModuleNotFoundError" in error