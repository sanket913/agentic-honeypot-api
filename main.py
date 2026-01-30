from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import re
import random

app = FastAPI(
    title="Agentic Honeypot API",
    description="Adaptive Scam Engagement & Intelligence Extraction",
    version="1.1"
)

API_KEY = "hp_live_9f3a72d1"

# ---------- Models ----------
class Message(BaseModel):
    sender: str
    text: str
    timestamp: Optional[str] = None

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

# ---------- Logic ----------
SCAM_KEYWORDS = [
    "block", "verify", "urgent", "upi",
    "account", "suspend", "otp", "password"
]

REPLIES = [
    "I did not receive any prior alert, can you explain?",
    "This sounds serious, what should I do now?",
    "Why is my account being blocked?",
    "Please clarify the issue in detail.",
    "Can you explain more about this verification?"
]

@app.post("/api/honeypot")
async def honeypot_endpoint(
    body: HoneypotRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = body.message.text.lower()

    keyword_hits = sum(1 for word in SCAM_KEYWORDS if word in text)
    scam_confidence = round(keyword_hits / len(SCAM_KEYWORDS), 2)
    scam_detected = scam_confidence > 0

    reply = random.choice(REPLIES) if scam_detected else "Thank you for the message."

    bank_accounts = re.findall(r"\b\d{12,16}\b", text)
    upi_ids = re.findall(r"\b[\w.-]+@[\w.-]+\b", text)
    phone_numbers = re.findall(r"\+91\d{10}", text)
    links = re.findall(r"https?://\S+", text)

    urgency_level = "High" if any(w in text for w in ["urgent", "immediately", "block"]) else "Medium"

    return {
        "status": "success",
        "honeypot_reply": reply,
        "scam_detected": scam_detected,
        "scam_confidence": scam_confidence,
        "engagement_stage": "trust_building" if scam_detected else "neutral",
        "agent_strategy": "delay_and_extract",
        "urgency_level": urgency_level,
        "entities_detected": {
            "bank_accounts": bank_accounts,
            "upi_ids": upi_ids,
            "phone_numbers": phone_numbers,
            "links": links
        }
    }
