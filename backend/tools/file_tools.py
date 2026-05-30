from pathlib import Path
WORKSPACE= Path("workspace/generated")

def write_file(filename:str, content:str):
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    file_path = WORKSPACE / filename
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

def read_file(filename:str):
    file_path = WORKSPACE/filename
    if not file_path.exists():
        raise FileNotFoundError(f"{filename} does not exist in workspace")
    with open(file_path,"r") as f:
        return f.read()

def list_files():
    if not WORKSPACE.exists():
        return []
    return [f.name for f in WORKSPACE.iterdir() if f.is_file()]

def is_safe_filename(filename:str):
    # Basic check to prevent ivalid filenames
    if filename.startswith("..") or "/" in filename or "\\" in filename:
        return False
    return True