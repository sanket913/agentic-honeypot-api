from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import random

app = FastAPI(
    title="Agentic Honeypot API",
    description="Adaptive Scam Engagement API",
    version="2.0"
)

API_KEY = "hp_live_9f3a72d1"

# ---------------- MODELS ----------------
class Message(BaseModel):
    sender: Optional[str] = "scammer"
    text: Optional[str] = "Your account will be blocked."
    timestamp: Optional[str] = None

class HoneypotRequest(BaseModel):
    sessionId: Optional[str] = None
    message: Optional[Message] = None
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

# ---------------- RESPONSES ----------------
REPLIES = [
    "Why is my account being blocked?",
    "What verification is required from my side?",
    "I did not receive any prior alert, can you explain?",
    "This sounds serious, what should I do now?",
    "Can you explain more?"
]

# ---------------- ENDPOINT ----------------
@app.post("/api/honeypot")
async def honeypot_endpoint(
    request: Request,
    x_api_key: str = Header(None)
):
    # API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        body = await request.json()
        text = body.get("message", {}).get("text", "").lower()
    except:
        text = ""
    reply = random.choice(REPLIES)
    return {
        "status": "success",
        "reply": reply
    }
    
@app.get("/")
def root():
    return {"status": "Agentic Honeypot API running"}
