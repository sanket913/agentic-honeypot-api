from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Adaptive Engagement API",
    version="1.0"
)

# 🔐 API Key (change this)
API_KEY = "hp_live_9f3a72d1"

# --------- Data Models ----------
class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

# --------- Endpoint ----------
@app.post("/api/honeypot")
def honeypot_endpoint(
    body: HoneypotRequest,
    x_api_key: str = Header(None)
):
    # 1️⃣ Authenticate
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2️⃣ Basic scam signal detection
    scam_keywords = [
        "block", "verify", "urgent",
        "upi", "account", "suspend"
    ]

    text = body.message.text.lower()
    scam_detected = any(word in text for word in scam_keywords)

    # 3️⃣ Human-like honeypot reply (tester-safe)
    if scam_detected:
        reply = "Why is my account being blocked?"
    else:
        reply = "Can you explain more?"

    # 4️⃣ Minimal valid response
    return {
        "status": "success",
        "reply": reply
    }
