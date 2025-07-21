import torch
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset

from .config import INTENTS 
from .state import rag_q
from .tts import speak_with_edge_tts
from .mistral_client import mistral_generate, generate_voice_reply

import asyncio

# Load intent model and encode intent embeddings
intent_model = SentenceTransformer("all-MiniLM-L6-v2")
INTENT_EMBEDDINGS = intent_model.encode(INTENTS, convert_to_tensor=True)

# Load FAQ dataset and encode FAQ question embeddings
ds = load_dataset("dltdojo/ecommerce-faq-chatbot-dataset")
faq_qs = list(ds["train"]["question"])
faq_as = list(ds["train"]["answer"])
faq_docs = [{"question": q, "answer": a} for q, a in zip(faq_qs, faq_as)]
FAQ_EMBEDDINGS = intent_model.encode(faq_qs, convert_to_tensor=True)

def detect_intent_and_rag(transcript):
    embedding = intent_model.encode(transcript, convert_to_tensor=True)

    # === Check for known intent ===
    cosine_scores = util.pytorch_cos_sim(embedding, INTENT_EMBEDDINGS)[0]
    score, idx = torch.max(cosine_scores, dim=0)
    score = score.item()

    if score > 0.6:
        intent = INTENTS[idx]
        print(f"🤖 Intent Detected: '{intent}' (score: {score:.2f})")
        response = generate_voice_reply(intent)
        asyncio.run(speak_with_edge_tts(response))
        return

    # === Fallback to FAQ RAG ===
    faq_scores = util.pytorch_cos_sim(embedding, FAQ_EMBEDDINGS)[0]
    top_score, top_idx = torch.max(faq_scores, dim=0)
    top_score = top_score.item()

    if top_score > 0.6:
        faq = faq_docs[top_idx]
        context = faq["answer"]
        rag_q.put((transcript, context, top_score))
    else:
        print("❓ No matching FAQ found. Try asking differently or connect with a human agent.")
