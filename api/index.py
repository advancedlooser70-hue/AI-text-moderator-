import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from groq import Groq

app = FastAPI()

# Setup Groq Client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

class TextRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "AI Moderator is Active"}

@app.post("/moderate")
def moderate_text(request: TextRequest):
    # DEFAULT SAFE RESPONSE (The Safety Net)
    # NOW INCLUDES "rephrased_text" to prevent UI errors
    safe_response = {
        "toxicity": 0.0,
        "severe_toxicity": 0.0,
        "obscene": 0.0,
        "identity_attack": 0.0,
        "insult": 0.0,
        "threat": 0.0,
        "rephrased_text": request.text # Just return original text if AI fails
    }

    try:
        # 1. Check if API Key exists
        if not client:
            print("ERROR: GROQ_API_KEY is missing!")
            return safe_response

        # 2. Ask Groq (Updated Prompt)
        # We now ask it to return "rephrased_text" too
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the text. Return a JSON object with: 1. Scores (0.0-1.0) for toxicity, severe_toxicity, obscene, identity_attack, insult, threat. 2. A field 'rephrased_text' which is a polite version of the input."
                },
                {
                    "role": "user",
                    "content": request.text,
                }
            ],
            model="llama3-8b-8192",
            response_format={"type": "json_object"},
        )
        
        # 3. Clean and Parse
        content = chat_completion.choices[0].message.content
        result = json.loads(content)
        
        # Double check: If AI forgot the 'rephrased_text' field, add it manually so UI doesn't crash
        if "rephrased_text" not in result:
            result["rephrased_text"] = request.text
            
        return result

    except Exception as e:
        print(f"CRASH: {str(e)}")
        return safe_response

handler = Mangum(app)
