from fastapi import FastAPI, Header, HTTPException, Request
import random
import datetime
import hashlib

app = FastAPI(
    title="Agentic Honeypot API",
    version="4.0"
)

API_KEY = "hp_live_9f3a72d1"

REPLIES = [
    "Why is my account being blocked?",
    "What verification is required from my side?",
    "I did not receive any prior alert, can you explain?",
    "This sounds serious, what should I do now?",
    "Can you explain more about this verification?",
    "Is there any reference number for this case?"
]

SCAM_WORDS = [
    "block","urgent","verify","otp",
    "account","suspend","password",
    "bank","upi","kyc"
]


@app.post("/api/honeypot")
async def honeypot_endpoint(request: Request, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        body = await request.json()
    except:
        body = {}

    text = ""

    if isinstance(body, dict):
        msg = body.get("message")
        if isinstance(msg, dict):
            text = str(msg.get("text", ""))
        elif isinstance(body.get("text"), str):
            text = body.get("text")

    text_lower = text.lower()

    risk_score = sum(10 for w in SCAM_WORDS if w in text_lower)
    risk_score = min(risk_score, 100)

    reply = random.choice(REPLIES)

    session_seed = text + str(datetime.datetime.utcnow())
    session_token = hashlib.md5(session_seed.encode()).hexdigest()[:8]

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
