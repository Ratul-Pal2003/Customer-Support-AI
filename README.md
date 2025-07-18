# Real-Time Customer Support Agent Assist & Resolution Bot

This project demonstrates a real-time AI assistant designed to support human agents during customer service calls. It listens to live audio, transcribes it, detects customer intent, performs RAG (Retrieval-Augmented Generation), and can respond with AI voice for predefined queries.

## 🚀 Features

- 🎙️ Real-time audio transcription using Whisper
- 🧠 Intent detection using HuggingFace NLI models
- 🔎 RAG (Retrieval-Augmented Generation) to fetch KB answers
- 🗣️ AI Voice responses using Edge-TTS
- 💬 Agent Assist UI using Streamlit
- 📦 Modular backend codebase (Python)

## 🗂 Project Structure

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


## ⚙️ Setup Instructions

1. **Clone the Repository**

   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. **Create and Activate Virtual environment**

python -m venv venv
source venv/bin/activate       # macOS/Linux
.\venv\Scripts\activate        # Windows

3. **Install Dependencies**

pip install -r requirements.txt

4. **Setup environment variables**

Create a .env file in the root folder.

Copy values from .env.example and insert your own credentials.

5. **Run the app Locally**

streamlit run streamlit_app.py


6. **Requirements**

Python 3.10+

FFmpeg installed and added to PATH

Hugging Face API key

Mistral (via Together API or HF Inference)

6. **Environment Variables**

HF_API_KEY=your_huggingface_key
TOGETHER_API_KEY=your_together_api_key
