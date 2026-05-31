from typing import TypedDict

class AgentState(TypedDict):
    task:str
    filename:str
    generated_code:str
    reviewed_code:str
    reviewed_result:str
    plan: str
    file_path:str
