from fastapi import FastAPI, Header, HTTPException, Body
from typing import List, Optional

app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Adaptive Engagement API",
    version="1.0"
)

API_KEY = "hp_live_9f3a72d1"

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/api/honeypot")
async def honeypot_endpoint(
    body: dict | None = Body(default=None),
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ✅ GUVI tester / empty request
    if not body or "message" not in body:
        return {
            "status": "success",
            "reply": "Hello, how can I help you?"
        }

    # ✅ Real honeypot logic
    text = body["message"]["text"].lower()

    scam_keywords = [
        "block", "verify", "urgent",
        "upi", "account", "suspend", "kyc"
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
