import os
import json  # <--- NEW: Added this tool
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
from groq import Groq

# 1. Setup the App
app = FastAPI()

# 2. Setup the Groq Client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class TextRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "AI Moderator is Active (Powered by Groq)"}

@app.post("/moderate")
def moderate_text(request: TextRequest):
    try:
        # 3. Send text to Groq API for analysis
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    # We ask for a JSON object with scores between 0.0 and 1.0
                    "content": "You are a content moderation API. Analyze the user's text. Return ONLY a JSON object with floating point scores (0.0 to 1.0) for: toxicity, severe_toxicity, obscene, identity_attack, insult, threat. Do not output any other text."
                },
                {
                    "role": "user",
                    "content": f"Analyze this text: {request.text}",
                }
            ],
            model="llama3-8b-8192",
            response_format={"type": "json_object"},
        )
        
        # 4. CRITICAL FIX: Convert the String response into a Real Object
        # Before: return chat_completion.choices[0].message.content  (Sent as "String")
        # After:  return json.loads(...)                             (Sent as Object)
        return json.loads(chat_completion.choices[0].message.content)
        
    except Exception as e:
        # If something breaks, print the error to the logs so we can see it
        print(f"Error: {e}")
        return {"error": str(e)}

# 5. Handler for Vercel
handler = Mangum(app)
