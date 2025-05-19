# ai/config/settings.py

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from pinecone import Pinecone

from ai.agents.summarizer_agent import MeetingSummaryAgent
from ai.agents.markdown_converter_agent import TemplateToMarkdownAgent
from ai.agents.report_builder_agent import FinalDocumentAgent

# -----------------------------
# 📁 경로 설정
# -----------------------------
# 프로젝트 루트 기준
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROMPT_DIR = os.path.join(BASE_DIR,"ai", "prompts")
UPLOAD_DIR = os.path.join(BASE_DIR,"ai", "uploads")
ENV_PATH = os.path.join(BASE_DIR,"ai", ".env")

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

# -----------------------------
# 🤖 에이전트 초기화
# -----------------------------
summary_agent = MeetingSummaryAgent(
    prompt_path=os.path.join(PROMPT_DIR, "summarizer_prompt.txt")
)

markdown_agent = TemplateToMarkdownAgent(
    vectorstore=vectorstore,
    prompt_path=os.path.join(PROMPT_DIR, "markdown_format_prompt.txt")
)

final_doc_agent = FinalDocumentAgent(
    vectorstore=vectorstore,
    prompt_path=os.path.join(PROMPT_DIR, "report_building_prompt.txt")
)
