import os
import json
import re # Used for cleaning text
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from groq import Groq

app = FastAPI()

# Setup Groq Client
# If the key is missing, this might fail, so we handle it inside the function
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
    # We start with this. If AI fails, we return this so the app works.
    safe_response = {
        "toxicity": 0.0,
        "severe_toxicity": 0.0,
        "obscene": 0.0,
        "identity_attack": 0.0,
        "insult": 0.0,
        "threat": 0.0
    }

    try:
        # 1. Check if API Key exists
        if not client:
            print("ERROR: GROQ_API_KEY is missing in Vercel Settings!")
            return safe_response

        # 2. Ask Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the text. Return a JSON object with scores (0.0 to 1.0) for: toxicity, severe_toxicity, obscene, identity_attack, insult, threat."
                },
                {
                    "role": "user",
                    "content": request.text,
                }
            ],
            model="llama3-8b-8192",
            response_format={"type": "json_object"},
        )
        
        # 3. Clean and Parse the Response
        raw_content = chat_completion.choices[0].message.content
        
        # Remove markdown backticks if they exist (Common AI error)
        clean_content = raw_content.replace("```json", "").replace("```", "").strip()
        
        # Parse into a real Dictionary
        result = json.loads(clean_content)
        return result

    except Exception as e:
        # If ANYTHING crashes, print error to Vercel logs but return SAFE to the user
        print(f"CRASH REPORT: {str(e)}")
        return safe_response

handler = Mangum(app)
