from typing import TypedDict

class AgentState(TypedDict):
    task:str
    filename:str
    generated_code:str
    reviewed_code:str
    reviewed_result:str
    plan: str
    file_path:str
    files: list[str]
    current_file: str
    current_file_index: int
    generated_files: list[str]
    project_context: str
