import os
import sys
import base64
from dotenv import load_dotenv

# 🔧 sys.path를 가장 먼저 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from ai.config import config  # ✅ 이제 문제 없음

# 1. 환경변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# 2. 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

# 3. 인덱스 설정
index_name = "vision-template-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(index_name)

# 4. 이미지 템플릿 정의
IMG_DIR = os.path.join(config.BASE_DIR, "ai", "images")
image_documents = [
    {"file": os.path.join(IMG_DIR, "basic_template.png"), "template_id": "basic_tem", "type": "template"},
]

# 5. GPT-Vision을 통한 설명 추출 함수
def describe_image_with_gpt_vision(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 이미지를 문서 템플릿의 레이아웃과 목적 중심으로 자세히 설명해줘."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content

# 6. 전체 이미지 처리 및 업로드
for doc in image_documents:
    print(f"🔍 GPT-Vision 설명 추출 중: {doc['file']}")
    description = describe_image_with_gpt_vision(doc["file"])
    print(f"✅ 설명 결과: {description[:100]}...")

    print(f"📡 임베딩 및 업로드 중: {doc['template_id']}")
    vector = embedding_model.embed_query(description)
    index.upsert([{
        "id": doc["template_id"],
        "values": vector,
        "metadata": {
            "template_id": doc["template_id"],
            "type": doc["type"],
            "source": os.path.basename(doc["file"]),
            "description": description
        }
    }])

print("✅ 이미지 기반 벡터 DB 구축 완료")
