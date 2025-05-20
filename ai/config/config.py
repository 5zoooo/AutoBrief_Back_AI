# ai/config/settings.py

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# -----------------------------
# 📁 경로 설정
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROMPT_DIR = os.path.join(BASE_DIR, "ai", "prompts")
UPLOAD_DIR = os.path.join(BASE_DIR, "ai", "uploads")
ENV_PATH = os.path.join(BASE_DIR, "ai", ".env")

# -----------------------------
# 🔐 환경 변수 로딩
# -----------------------------
load_dotenv(dotenv_path=ENV_PATH)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = "meeting-template-index"

# -----------------------------
# 🔗 Pinecone & 임베딩
# -----------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = PineconeVectorStore(index=index, embedding=embedding_model, text_key="text")
