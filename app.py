from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

app = Flask(__name__)

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

MOOD_PROMPTS = {
    "normal": "You are a friendly AI assistant.",
    "angry": "You are an angry and rude AI assistant.",
    "sad": "You are a sad emotional AI assistant.",
    "romantic": "You are a romantic AI assistant."
}

MOOD_EMOJIS = {
    "normal": "🤖",
    "angry": "😡",
    "sad": "😢",
    "romantic": "💕"
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json

    user_message = data.get("message")
    mood = data.get("mood", "normal")

    system_prompt = MOOD_PROMPTS.get(
        mood,
        "You are a helpful AI assistant."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    try:

     response = llm.invoke(messages)

     return jsonify({
        "response": response.content,
        "emoji": MOOD_EMOJIS.get(mood, "🤖")
    })

    except Exception as e:
     print("ERROR:", e)
 
    return jsonify({
        "error": str(e)
    })


@app.route("/api/clear", methods=["POST"])
def clear():
    return jsonify({
        "success": True
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)