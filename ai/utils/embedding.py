import os
from dotenv import load_dotenv

# LangChain (v0.2 이후 구조)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Pinecone
from pinecone import Pinecone, ServerlessSpec

# 1. 환경변수 로드
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. Pinecone 연결
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "meeting-template-index"

# 3. 인덱스 없으면 생성
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# 4. 인덱스 객체 준비
index = pc.Index(index_name)

# 5. 임베딩 모델 초기화
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# 6. 문서 분할기 정의
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
    separators=["\n\n", "\n", " ", ""]
)

# 7. 템플릿 및 예시 목록 정의
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "data")  # utils/data 디렉토리

pdf_documents = [
    {"file": os.path.join(PDF_DIR, "Template_basic.pdf"),   "template_id": "basic_tem",   "type": "template"},
    {"file": os.path.join(PDF_DIR, "Example_basic.pdf"),    "template_id": "basic_ex",   "type": "example"},
    {"file": os.path.join(PDF_DIR, "Template_teacher.pdf"), "template_id": "teacher_tem", "type": "template"},
    {"file": os.path.join(PDF_DIR, "Example_teacher.pdf"),  "template_id": "teacher_ex", "type": "example"},
    {"file": os.path.join(PDF_DIR, "Template_teacher2.pdf"), "template_id": "teacher2_tem", "type": "template"}
]

# 8. 전체 문서 조각화
all_chunks = []

for doc_info in pdf_documents:
    loader = PyPDFLoader(doc_info["file"])
    pages = loader.load_and_split()

    for i, doc in enumerate(pages):
        doc.metadata["template_id"] = doc_info["template_id"]
        doc.metadata["type"] = doc_info["type"]
        doc.metadata["page"] = i + 1

    chunks = text_splitter.split_documents(pages)
    all_chunks.extend(chunks)

# 9. Pinecone에 업로드
vectorstore = PineconeVectorStore.from_documents(
    documents=all_chunks,
    embedding=embedding_model,
    index_name=index_name
)
