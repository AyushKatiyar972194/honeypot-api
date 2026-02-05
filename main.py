from fastapi import FastAPI, Header, HTTPException
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY", "hackathon123")

@app.post("/honeypot")
def honeypot(payload: dict = None, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Safe defaults
    text = ""

    if payload and isinstance(payload, dict):
        msg = payload.get("message", {})
        if isinstance(msg, dict):
            text = msg.get("text", "")

    # Simple scam-style human reply
    reply = "Why is my account being suspended?"

    return {
        "status": "success",
        "reply": reply
    }
