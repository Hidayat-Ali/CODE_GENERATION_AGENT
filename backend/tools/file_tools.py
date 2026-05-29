from pathlib import Path
WORKSPACE= Path("workspace/generated")

def write_file(filename:str, content:str):
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    file_path = WORKSPACE / filename
    with open(file_path, "w") as f:
        f.write(content)
    return file_path