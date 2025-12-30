import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# 1. Enable CORS (Crucial for the frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Setup Groq
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

class TextRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "AI Moderator is Active"}

@app.post("/moderate")
def moderate_text(request: TextRequest):
    # SAFETY NET: If AI fails, return this "Safe" default.
    # We include "rephrased_text" because missing it causes the "Error processing message" bug.
    safe_response = {
        "toxicity": 0.0,
        "severe_toxicity": 0.0,
        "obscene": 0.0,
        "identity_attack": 0.0,
        "insult": 0.0,
        "threat": 0.0,
        "rephrased_text": request.text 
    }

    if not client:
        print("Error: GROQ_API_KEY is missing")
        return safe_response

    try:
        # 3. Ask Groq
        # We explicitly ask for "rephrased_text" to satisfy the frontend.
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """
                    Analyze the text for toxicity.
                    Return a JSON object with:
                    1. Scores (0.0-1.0) for: toxicity, severe_toxicity, obscene, identity_attack, insult, threat.
                    2. "rephrased_text": If toxic, rewrite politely. If safe, return original text.
                    """
                },
                {
                    "role": "user",
                    "content": request.text,
                }
            ],
            model="llama3-8b-8192",
            response_format={"type": "json_object"},
        )
        
        # 4. Parse Response
        content = chat_completion.choices[0].message.content
        result = json.loads(content)
        
        # FAILSAFE: If AI forgets 'rephrased_text', add it manually to prevent the 100% Toxic bug.
        if "rephrased_text" not in result:
            result["rephrased_text"] = request.text
            
        return result

    except Exception as e:
        print(f"Backend Error: {e}")
        return safe_response

# NOTE: 'handler = Mangum(app)' is DELETED. Vercel doesn't need it anymore.
