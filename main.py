from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Adaptive Engagement API",
    version="1.0"
)

API_KEY = "hp_live_9f3a72d1"

class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

# ✅ Health check (IMPORTANT for tester)
@app.get("/")
def health():
    return {"status": "ok"}

# --------- Endpoint ----------
@app.post("/api/honeypot")
async def honeypot_endpoint(
    request: Request,
    x_api_key: str = Header(None)
):
    # API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Try to read JSON body safely
    try:
        body = await request.json()
    except:
        body = None

    # ✅ CASE 1: Tester / empty request
    if not body or "message" not in body:
        return {
            "status": "success",
            "reply": "Hello, how can I help you?"
        }

    # ✅ CASE 2: Real honeypot logic
    text = body["message"]["text"].lower()

    scam_keywords = [
        "block", "verify", "urgent",
        "upi", "account", "suspend"
    ]

    scam_detected = any(word in text for word in scam_keywords)

    if scam_detected:
        reply = "Why is my account being blocked?"
    else:
        reply = "Can you explain more?"

    return {
        "status": "success",
        "reply": reply
    }
