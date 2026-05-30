from typing import TypedDict

class AgentState(TypedDict):
    task:str
    filename:str
    reviewed_code:str
    generated_code:str
    file_path:str
