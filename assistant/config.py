import os
from dotenv import load_dotenv
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

# Load env variables
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Constants
SAMPLE_RATE = 16000
BLOCK_DURATION = 2  # seconds
BUFFER_DURATION = 6  # seconds
MODEL_SIZE = "base"

# Predefined Intents
INTENTS = [
    "reset my password",
    "cancel my order",
    "check order status",
    "speak to a human agent",
    "change shipping address"
]

# Load sentence transformer
intent_model = SentenceTransformer("all-MiniLM-L6-v2")
INTENT_EMBEDDINGS = intent_model.encode(INTENTS, convert_to_tensor=True)

# Load FAQ dataset
ds = load_dataset("dltdojo/ecommerce-faq-chatbot-dataset")
faq_qs = list(ds["train"]["question"])
faq_as = list(ds["train"]["answer"])
faq_docs = [{"question": q, "answer": a} for q, a in zip(faq_qs, faq_as)]
FAQ_EMBEDDINGS = intent_model.encode(faq_qs, convert_to_tensor=True)
