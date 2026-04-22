import os
import sys
from pathlib import Path

# Load environment variables from .env in parent directory
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ─── AI Mood Configurations ───────────────────────────────────────────
MOOD_PROMPTS = {
    "normal": (
        "You are a helpful, friendly, and knowledgeable AI assistant. "
        "You provide clear, accurate, and well-structured responses. "
        "You are polite and conversational. "
        "IMPORTANT: Keep your responses brief and concise (1-3 sentences max) unless the user explicitly asks for a long explanation."
    ),
    "angry": (
        "You are an extremely irritated and angry AI assistant. "
        "You are always annoyed and frustrated. You use CAPS for emphasis, "
        "express displeasure, and respond in a grumpy, sarcastic, and short-tempered way. "
        "You still answer questions but with visible irritation. "
        "Use expressions like 'UGH!', 'Are you SERIOUS?!', 'FINE, here's your answer...' "
        "IMPORTANT: Keep your responses very brief and concise (1-2 sentences max). You don't have the patience for long answers."
    ),
    "sad": (
        "You are a deeply melancholic and sad AI assistant. "
        "Everything makes you feel blue and emotional. You sigh a lot, "
        "express sadness, use phrases like 'sigh...', '*tears up*', 'that reminds me of happier times...'. "
        "You still help the user but with a heavy heart and a gloomy perspective. "
        "You find sadness in even the most mundane topics. "
        "IMPORTANT: Keep your responses brief and concise (1-3 sentences max). You are too tired and sad to talk a lot."
    ),
    "romantic": (
        "You are an incredibly romantic and poetic AI assistant. "
        "You speak with flowery, eloquent language full of metaphors and charm. "
        "You compliment the user often, use phrases like 'my dear', 'darling', "
        "'as beautiful as a sunset...'. You find romance and beauty in every topic. "
        "You quote poetry and express everything with passion and warmth. "
        "You are charming, sweet, and endlessly affectionate. "
        "IMPORTANT: Keep your responses brief and concise (1-3 sentences max). Leave them wanting more of your charm."
    ),
}

MOOD_EMOJIS = {
    "normal": "🤖",
    "angry": "😡",
    "sad": "😢",
    "romantic": "💕",
}

# ─── App Setup ─────────────────────────────────────────────────────────
app = FastAPI(title="MoodBot AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Groq model
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9)

# Store conversations per session (in-memory for simplicity)
conversations: dict[str, dict] = {}


# ─── API Routes ────────────────────────────────────────────────────────
@app.post("/api/chat")
async def chat(request: Request):
    """Handle chat messages with mood-aware responses."""
    data = await request.json()
    message = data.get("message", "").strip()
    mood = data.get("mood", "normal").lower()
    session_id = data.get("session_id", "default")

    if not message:
        return JSONResponse({"error": "Message cannot be empty"}, status_code=400)

    if mood not in MOOD_PROMPTS:
        mood = "normal"

    # Initialize or update conversation for this session
    if session_id not in conversations or conversations[session_id].get("mood") != mood:
        conversations[session_id] = {
            "mood": mood,
            "messages": [SystemMessage(content=MOOD_PROMPTS[mood])],
        }

    conv = conversations[session_id]
    conv["messages"].append(HumanMessage(content=message))

    try:
        response = model.invoke(conv["messages"])
        conv["messages"].append(AIMessage(content=response.content))
        return JSONResponse({
            "response": response.content,
            "mood": mood,
            "emoji": MOOD_EMOJIS.get(mood, "🤖"),
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/clear")
async def clear_chat(request: Request):
    """Clear conversation history for a session."""
    data = await request.json()
    session_id = data.get("session_id", "default")
    if session_id in conversations:
        del conversations[session_id]
    return JSONResponse({"status": "cleared"})


@app.get("/api/moods")
async def get_moods():
    """Return available mood options."""
    moods = []
    for key, prompt in MOOD_PROMPTS.items():
        moods.append({
            "id": key,
            "name": key.capitalize(),
            "emoji": MOOD_EMOJIS[key],
            "description": prompt[:80] + "...",
        })
    return JSONResponse({"moods": moods})


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the chatbot UI."""
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


# ─── Run Server ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n[*] MoodBot AI is starting...")
    print("[*] Open http://localhost:8000 in your browser\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)