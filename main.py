from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import re
import random

app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Adaptive Engagement API",
    version="1.0"
)

API_KEY = "hp_live_9f3a72d1"

# --------- Models ----------
class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

# Scam detection keywords
SCAM_KEYWORDS = ["block", "verify", "urgent", "upi", "account", "suspend", "otp", "password"]

# Dynamic human-like responses
REPLIES = [
    "Why is my account being blocked?",
    "Can you explain more?",
    "I did not receive any alerts before, can you clarify?",
    "Please provide more details.",
    "I am concerned, what exactly happened?"
]

# --------- Honeypot Endpoint ----------
@app.post("/api/honeypot")
async def honeypot_endpoint(
    body: HoneypotRequest,
    x_api_key: str = Header(None)
):
    # Validate API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = body.message.text.lower()

    # Scam detection confidence
    keyword_hits = sum(word in text for word in SCAM_KEYWORDS)
    scam_confidence = round(min(keyword_hits / len(SCAM_KEYWORDS), 1.0), 2)
    scam_detected = scam_confidence > 0

    # Dynamic human-like reply
    reply = random.choice(REPLIES) if scam_detected else "Thank you for the message, noted."

    # Extract intelligence
    bank_accounts = re.findall(r"\b\d{12,16}\b", text)
    upi_ids = re.findall(r"\b[\w.-]+@[\w.-]+\b", text)
    phone_numbers = re.findall(r"\+91[\d]{10}", text)
    links = re.findall(r"https?://\S+", text)

    # Risk & scam type
    scam_type = "Banking / UPI Fraud" if any([bank_accounts, upi_ids]) else "Phishing / Fake Offer"
    urgency_level = "High" if any(word in text for word in ["urgent", "immediately", "block"]) else "Medium"

    return {
        "status": "success",
        "reply": reply,
        "scam_detected": scam_detected,
        "scam_confidence": scam_confidence,
        "scam_type": scam_type,
        "urgency_level": urgency_level,
        "entities_detected": {
            "bank_account_numbers": bank_accounts,
            "upi_ids": upi_ids,
            "phone_numbers": phone_numbers,
            "links": links
        }
    }
