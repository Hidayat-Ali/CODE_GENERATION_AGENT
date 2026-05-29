from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def generate_response(prompt:str):
    stream_response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        
        contents=prompt, 
    )
    for chunk in stream_response:
        if chunk.text:
            yield chunk.text
