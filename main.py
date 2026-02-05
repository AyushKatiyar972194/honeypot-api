import os
from fastapi import FastAPI, Header, HTTPException
import re

app = FastAPI(title="Agentic Honeypot API")

API_KEY = "hackathon123"   # you will use this while submitting

# ---------------- SCAM DETECTION ----------------
def detect_scam(text: str) -> bool:
    scam_keywords = [
        "kyc", "blocked", "urgent", "verify",
        "upi", "payment", "click", "link", "bank"
    ]
    score = sum(1 for k in scam_keywords if k in text.lower())
    return score >= 2

# ---------------- INTELLIGENCE EXTRACTION ----------------
def extract_intelligence(text: str):
    upi_ids = re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text)
    urls = re.findall(r"https?://\S+", text)
    bank_accounts = re.findall(r"\b\d{9,18}\b", text)

    return {
        "upi_ids": list(set(upi_ids)),
        "bank_accounts": list(set(bank_accounts)),
        "phishing_urls": list(set(urls))
    }

# ---------------- AUTONOMOUS AGENT ----------------
def agent_response():
    return "Okay sir, please explain the process clearly."

# ---------------- API ENDPOINT ----------------
@app.post("/honeypot")
def honeypot(
    payload: dict,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    message = payload.get("message", "")
    conversation_id = payload.get("conversation_id", "unknown")

    scam_detected = detect_scam(message)
    extracted = extract_intelligence(message)

    return {
        "conversation_id": conversation_id,
        "scam_detected": scam_detected,
        "agent_activated": scam_detected,
        "agent_reply": agent_response() if scam_detected else "Thank you.",
        "extracted_intelligence": extracted,
        "metrics": {
            "conversation_turns": 1
        }
    }
