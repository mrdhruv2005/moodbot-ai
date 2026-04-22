# 🤖 MoodBot AI

An AI-powered chatbot that responds based on the user's selected mood.
This project uses LLMs to generate dynamic and emotionally adaptive responses.

---

## 🌟 Features

* 🎭 **Mood-Based Responses**

  * Normal 😐
  * Romantic ❤️
  * Angry 😡
  * Sad 😢

* 💬 Context-aware chatbot replies

* ⚡ Fast response generation using AI models

* 🧠 Custom personality switching based on mood

---

## 🛠️ Tech Stack

* Python 🐍
* LangChain
* Groq API (LLM)
* dotenv (for environment variables)

---

## 🚀 How It Works

1. User selects a mood
2. The chatbot adjusts its personality
3. AI model generates response based on selected mood

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/mrdhruv2005/moodbot-ai.git
cd moodbot-ai
```

### 2. Create virtual environment

```bash
uv venv
```

### 3. Activate environment

#### Windows:

```bash
.venv\Scripts\activate
```

#### Mac/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
uv pip install -r requirements.txt
```

---

## 🔑 Setup Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

```bash
python chatbot.py
```

---

## 📂 Project Structure

```
MoodBot-AI/
│── chatbot.py
│── requirements.txt
│── .env
│── README.md
```

---

## 💡 Example Usage

```
Select Mood: Romantic ❤️
User: Hi
Bot: Hey love, how was your day? 💖
```

---

## ⚠️ Notes

* Make sure your API key is valid
* Do not share your `.env` file publicly

---

## 📈 Future Improvements

* Web UI (Streamlit / React)
* Voice interaction 🎤
* Memory-based conversations
* More moods & personality tuning

---

## 👨‍💻 Author

Dhruv Garg

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
