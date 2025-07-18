# Real-Time Customer Support Agent Assist & Resolution Bot

This project demonstrates a real-time AI assistant designed to support human agents during customer service calls. It listens to live audio, transcribes it, detects customer intent, performs RAG (Retrieval-Augmented Generation), and can respond with AI voice for predefined queries.

## 🚀 Features

- 🎙️ Real-time audio transcription using Whisper
- 🧠 Intent detection using HuggingFace NLI models
- 🔎 RAG (Retrieval-Augmented Generation) to fetch KB answers
- 🗣️ AI Voice responses using Edge-TTS
- 📦 Modular backend codebase (Python)

## 🗂 Project Structure
```bash
AI PRJ/
├── assistant/
│ ├── audio.py
│ ├── config.py
│ ├── intent_rag.py
│ ├── main.py
│ ├── mistral_client.py
│ ├── rag_handler.py
│ ├── state.py
│ ├── transcription.py
│ └── tts.py
├── .env.example
├── requirements.txt
├── streamlit_app.py
├── README.md
├── .gitignore
└── venv/ (ignored)
```

## ⚙️ Setup Instructions

1. **Clone the Repository**
```bash
   git clone https://github.com/Ratul-Pal2003/Customer-Support-AI.git
   cd Customer-Support-AI
```

2. **Create and Activate Virtual environment**

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
.\venv\Scripts\activate        # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**

- Create a .env file in the root folder.

- Copy values from .env.example and insert your own credentials.



## Requirements

- Python 3.10+

- FFmpeg installed and added to PATH

- Hugging Face API key

- Mistral (via HF Inference)

6. **Environment Variables**
```bash
HF_API_KEY=your_huggingface_key
```