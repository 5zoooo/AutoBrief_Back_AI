import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from pinecone import Pinecone

# 1. 환경변수 로드
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = "meeting-template-index"

# 2. Pinecone 연결 및 인덱스 가져오기
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# 3. 임베딩 모델 초기화
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# 4. 기존 벡터 DB에서 검색할 수 있도록 vectorstore 생성
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embedding_model,
    text_key="text"  # 기본적으로 text라는 key로 저장됨 (문서 내용 필드)
)

# 5. 쿼리 입력 → 유사한 문서 검색
query = "교사 교육에 관련된 문서를 보여줘"
results = vectorstore.similarity_search(query, k=3)

# 6. 결과 출력
print("\n🔍 검색 결과:")
for i, doc in enumerate(results, 1):
    print(f"\n--- 결과 {i} ---")
    print(f"[페이지] {doc.metadata.get('page')} | [유형] {doc.metadata.get('type')} | [템플릿] {doc.metadata.get('template_id')}")
    print(f"{doc.page_content[:300]}...")  # 앞부분 미리보기
