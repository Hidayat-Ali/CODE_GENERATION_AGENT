from click import prompt
from fastapi import FastAPI
from pydantic import BaseModel
from services.gemnnii_service import generate_response
from fastapi.responses import StreamingResponse
from tools.file_tools import write_file

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "message": "Code Agent Backend Running"
    }
@app.post("/chat")
async def chat(req:ChatRequest):
    response = generate_response(req.message)
    return StreamingResponse(response, media_type="text/plain")

@app.post("/generate-file")
def generate_file(req:ChatRequest):
    prompt = f"""
        Generate ONLY executable Python code.

        No explanations.
        No markdown.
        No comments outside code.

        Task:
        {req.message}
        """
    code = "".join(generate_response(prompt))
    file_path = write_file("generated_code.py", code)
    return {"file_path": str(file_path)}