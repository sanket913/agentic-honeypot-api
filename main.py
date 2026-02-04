from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import random
import uuid
from datetime import datetime

app = FastAPI(
    title="Agentic Honeypot API",
    description="Adaptive Scam Engagement API",
    version="3.1"
)

API_KEY = "hp_live_9f3a72d1"

class Message(BaseModel):
    sender: Optional[str] = "scammer"
    text: Optional[str] = ""
    timestamp: Optional[int] = None

class HoneypotRequest(BaseModel):
    sessionId: Optional[str] = None
    message: Optional[Message] = Message()
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

REPLIES = [
    "Why is my account being blocked?",
    "Which branch issued this alert?",
    "What verification is required from my side?",
    "I did not receive any prior alert, can you explain?",
    "Can you confirm this from official support?"
]

@app.post("/api/honeypot")
async def honeypot_endpoint(
    body: HoneypotRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = (body.message.text or "").lower()

    scam_words = ["bank", "verify", "otp", "urgent", "block", "kyc"]
    score = sum(word in text for word in scam_words)

    reply = random.choice(REPLIES)

    return {
        "status": "success",
        "reply": reply,
        "risk_score": score * 20,
        "session_token": str(uuid.uuid4())[:8],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/")
def root():
    return {"status": "running"}
