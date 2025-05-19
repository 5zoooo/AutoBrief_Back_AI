import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as PineconeVectorStore
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

# 7. 회의록 템플릿 PDF 목록 + 명시적 메타데이터 지정
pdf_templates = [
    {"file": "Template_Executive.pdf", "template_id": "exec", "template_name": "executive_summary"},
    {"file": "Template_Discussion.pdf", "template_id": "discussion", "template_name": "team_discussion"},
    {"file": "Template_TechSpec.pdf", "template_id": "tech", "template_name": "technical_spec"}
]

# 8. 전체 분할된 문서 저장 리스트
all_chunks = []

for tpl in pdf_templates:
    loader = PyPDFLoader(tpl["file"])
    pages = loader.load_and_split()

    for i, doc in enumerate(pages):
        doc.metadata["template_id"] = tpl["template_id"]
        doc.metadata["template_name"] = tpl["template_name"]
        doc.metadata["page"] = i + 1

    chunks = text_splitter.split_documents(pages)
    all_chunks.extend(chunks)

# 9. Pinecone에 벡터 업로드
vectorstore = PineconeVectorStore.from_documents(
    documents=all_chunks,
    embedding=embedding_model,
    index_name=index_name
)
