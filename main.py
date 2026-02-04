from fastapi import FastAPI, Header, HTTPException, Request, Body
from typing import Optional, Dict, Any
import random, datetime, hashlib

app = FastAPI(title="Agentic Honeypot API", version="4.1")

API_KEY = "hp_live_9f3a72d1"

REPLIES = [
    "Why is my account being blocked?",
    "What verification is required from my side?",
    "I did not receive any prior alert, can you explain?",
    "This sounds serious, what should I do now?"
]

SCAM_WORDS = ["block","urgent","verify","otp","account","suspend","bank","upi"]


@app.post("/api/honeypot")
async def honeypot_endpoint(
    request: Request,
    body: Optional[Dict[str, Any]] = Body(default=None),
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if body is None:
        try:
            body = await request.json()
        except:
            body = {}

    text = ""
    msg = body.get("message", {})
    if isinstance(msg, dict):
        text = str(msg.get("text", ""))

    text_lower = text.lower()

    risk_score = min(sum(10 for w in SCAM_WORDS if w in text_lower), 100)

    reply = random.choice(REPLIES)

    token_seed = text + str(datetime.datetime.utcnow())
    session_token = hashlib.md5(token_seed.encode()).hexdigest()[:8]

    return {
        "status": "success",
        "reply": reply,
        "risk_score": risk_score,
        "session_token": session_token,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@app.get("/")
def root():
    return {"status": "running"}
