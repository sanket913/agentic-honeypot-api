from fastapi import FastAPI, Header, HTTPException, Request
import random
import json
import uuid
from datetime import datetime

app = FastAPI(
    title="Agentic Honeypot API",
    description="Adaptive Scam Engagement API",
    version="3.0"
)

API_KEY = "hp_live_9f3a72d1"

SCAM_PATTERNS = {
    "bank": ["bank", "account", "blocked", "verify", "kyc"],
    "payment": ["payment", "upi", "transaction", "refund"],
    "otp": ["otp", "code", "password"],
    "lottery": ["lottery", "winner", "prize"],
    "tech": ["support", "remote", "device", "virus"]
}

REPLY_BANK = [
    "This is unexpected. Can you confirm last 4 digits?",
    "Which branch issued this alert?",
    "Why was I not notified earlier?",
    "What verification is needed now?"
]

REPLY_PAYMENT = [
    "Which transaction are you referring to?",
    "I made multiple payments today, be specific.",
    "Can you share the reference number?"
]

REPLY_OTP = [
    "I did not receive any code yet.",
    "Resend the OTP please.",
    "How long is the OTP valid?"
]

REPLY_LOTTERY = [
    "I never entered any contest.",
    "Which organization selected me?",
    "Is there an official website link?"
]

REPLY_TECH = [
    "Which device shows the issue?",
    "Can you describe the problem in detail?",
    "I need proof before proceeding."
]

REPLY_GENERIC = [
    "Can you clarify that?",
    "Please provide more details.",
    "I am not convinced yet.",
    "Explain step by step."
]

def detect_category(text):
    for cat, words in SCAM_PATTERNS.items():
        for w in words:
            if w in text:
                return cat
    return "generic"

def pick_reply(category):
    if category == "bank":
        return random.choice(REPLY_BANK)
    if category == "payment":
        return random.choice(REPLY_PAYMENT)
    if category == "otp":
        return random.choice(REPLY_OTP)
    if category == "lottery":
        return random.choice(REPLY_LOTTERY)
    if category == "tech":
        return random.choice(REPLY_TECH)
    return random.choice(REPLY_GENERIC)

@app.get("/")
async def root():
    return {"status": "Agentic Honeypot API running"}

@app.post("/api/honeypot")
async def honeypot_endpoint(request: Request, x_api_key: str = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body_text = ""

    try:
        raw = await request.body()
        if raw:
            data = json.loads(raw)
            if isinstance(data, dict):
                body_text = str(data.get("message", {}).get("text", "")).lower()
    except:
        body_text = ""

    category = detect_category(body_text)
    reply = pick_reply(category)

    engagement_score = random.randint(70, 95)

    return {
        "status": "success",
        "reply": reply,
        "category_detected": category,
        "engagement_score": engagement_score,
        "session_token": str(uuid.uuid4())[:8],
        "timestamp": datetime.utcnow().isoformat()
    }
