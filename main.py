from fastapi import FastAPI, Header, HTTPException, Request
import re
import random
from typing import List, Dict, Any

app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Adaptive Engagement API",
    version="1.0"
)

API_KEY = "hp_live_9f3a72d1"

# Scam detection keywords
SCAM_KEYWORDS = [
    "block", "verify", "urgent", "upi", "account",
    "suspend", "otp", "password", "kyc", "immediately"
]

# Human-like adaptive replies
REPLIES = [
    "Why is my account being blocked?",
    "I did not receive any prior alert, can you explain?",
    "This sounds serious, what should I do now?",
    "Please clarify the issue in detail.",
    "What verification is required from my side?"
]

# ----------------- Honeypot Endpoint -----------------
@app.post("/api/honeypot")
async def honeypot_endpoint(
    request: Request,
    x_api_key: str = Header(None)
):
    # -------- API KEY VALIDATION --------
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # -------- SAFE BODY PARSING --------
    try:
        body: Dict[str, Any] = await request.json()
    except:
        body = {}

    # -------- HANDLE EMPTY / INVALID REQUEST --------
    if not body or "message" not in body:
        return {
            "status": "ok",
            "note": "Honeypot active and listening",
            "reply": "Hello, how can I help you today?"
        }

    message = body.get("message", {})
    text = message.get("text", "").lower()

    # -------- SCAM DETECTION --------
    keyword_hits = sum(word in text for word in SCAM_KEYWORDS)
    scam_confidence = round(min(keyword_hits / len(SCAM_KEYWORDS), 1.0), 2)
    scam_detected = scam_confidence > 0

    # -------- ENTITY EXTRACTION --------
    bank_accounts = re.findall(r"\b\d{12,16}\b", text)
    upi_ids = re.findall(r"\b[\w.-]+@[\w.-]+\b", text)
    phone_numbers = re.findall(r"\+91\d{10}", text)
    links = re.findall(r"https?://\S+", text)

    # -------- SCAM CLASSIFICATION --------
    if bank_accounts or upi_ids:
        scam_type = "Banking / UPI Fraud"
    elif links:
        scam_type = "Phishing Scam"
    else:
        scam_type = "Social Engineering Scam"

    urgency_level = "High" if any(
        word in text for word in ["urgent", "immediately", "block"]
    ) else "Medium"

    # -------- ADAPTIVE HUMAN RESPONSE --------
    reply = random.choice(REPLIES) if scam_detected else "Thank you for the information."

    # -------- FINAL RESPONSE --------
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
