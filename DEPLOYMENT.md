# Deployment Guide for Chat Toxicity Moderator

## Deploying on Vercel

This application can be deployed on Vercel, but there are important considerations due to the machine learning models used.

### Current Limitations with Vercel Deployment

⚠️ **Important Note**: The current implementation uses large ML models (Detoxify for toxicity detection and T5 for rephrasing) that:
- Take a long time to load (exceeding Vercel's serverless function timeout limits)
- Are too large for Vercel's deployment package size limits
- May cause cold start issues

### Recommended Deployment Options

#### Option 1: Vercel with External API (Recommended)

1. **Deploy the ML models separately** using a platform that supports larger applications:
   - Google Cloud Run
   - AWS Lambda with larger memory
   - Azure Functions
   - Railway
   - Render

2. **Update the Vercel deployment** to call your external API endpoints instead of running models locally

3. **Update the API code** to make requests to your hosted ML service instead of loading models locally

#### Option 2: Alternative Hosting Platforms

For full functionality with local ML models, consider these platforms:

- **Railway**: Better support for Python applications with ML dependencies
- **Render**: Supports larger applications and longer startup times
- **Google Cloud Run**: Good for containerized ML applications
- **AWS Elastic Beanstalk**: Traditional hosting with full Python support

### Vercel Deployment Steps (Simplified Version)

If you want to deploy a simplified version to Vercel:

1. **Create a new API that calls external services** instead of using local models:

```python
# api/moderate.py
import os
import requests
from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.post("/moderate")
async def moderate(msg: Message):
    # Call external toxicity detection API (e.g., Google Perspective API)
    # Or your own hosted ML service
    # This is a placeholder implementation
    text = msg.text.strip()
    
    # Simplified logic for demo purposes
    toxic_keywords = ["idiot", "stupid", "hate", "kill"]
    is_toxic = any(keyword in text.lower() for keyword in toxic_keywords)
    
    if is_toxic:
        # Call external rephrasing API or use simple replacement
        rephrased = text.replace("idiot", "misguided person").replace("stupid", "unwise")
        return {
            "allowed": False,
            "score": 0.8,
            "original": text,
            "rephrased": rephrased
        }
    else:
        return {
            "allowed": True,
            "score": 0.1,
            "text": text
        }

@app.get("/")
async def root():
    return {"message": "Toxicity Moderator API (Simplified for Vercel)"}

handler = Mangum(app)
```

2. **Update requirements.txt**:
```txt
fastapi
python-multipart
mangum
requests
```

3. **Deploy to Vercel**:
```bash
vercel --prod
```

### Environment Variables

For production deployment, add these environment variables:

- `GROQ_API_KEY`: For better rephrasing quality (optional)
- `PERSPECTIVE_API_KEY`: For external toxicity detection (if using Google Perspective API)

### Frontend Deployment

The frontend (HTML files in the `public` directory) will work correctly on Vercel and serve the user interface.

## Deployment Configuration

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/moderate.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.9"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/moderate",
      "dest": "api/moderate.py"
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1",
      "headers": {
        "Cache-Control": "public, max-age=31536000"
      }
    }
  ]
}
```

## Alternative: Docker Deployment

For full functionality with local models, consider using Docker:

1. Create a Dockerfile
2. Deploy on platforms that support Docker containers
3. Use platforms like Railway, Render, or AWS ECS

## Conclusion

While the application can be deployed on Vercel, the full ML functionality requires alternative hosting solutions due to model size and initialization time constraints. The frontend components work perfectly with Vercel's static hosting.