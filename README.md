# AutoBrief_Back_AI

**AutoBrief_Back_AI**는 오디오 파일(mpeg)을 업로드하면 AI가 지정된 템플릿과 파일 형식(docx, pdf, txt)으로 회의 요약문을 생성하고, 결과 문서를 다운로드할 수 있는 백엔드 API 서버입니다.

---

<br>

## 빠른 시작 (Quick Start)

1. **가상환경 설정 (권장)**
    ```bash
    # 가상환경 생성
    python -m venv venv
    
    # 가상환경 활성화 (macOS/Linux)
    source venv/bin/activate
    
    # 가상환경 활성화 (Windows)
    # venv\Scripts\activate
    ```

2. **의존성 설치**
    ```bash
    pip install -r requirements.txt
    ```
2. **환경 변수 설정**
    - `.env` 파일을 프로젝트 루트에 복사/생성 후 값 입력
3. **서버 실행**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
4. **Swagger UI 접속**
    - [http://localhost:8000/docs](http://localhost:8000/docs)
  
<br>

## API 명세 및 사용 예시

### 1. 문서 생성 (POST `/api/v1/generate-document`)

- **curl 예시**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/generate-document" \
      -F "file=@sample.mpeg" \
      -F "template=meeting_minutes" \
      -F "file_format=docx" \
      -F "filename=회의록_2025"
    ```
- **성공 응답**
    ```json
    {
      "download_url": "/api/v1/download/1?file_format=docx"
    }
    ```

### 2. 문서 다운로드 (GET `/api/v1/download/1?file_format=docx`)

- **curl 예시**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/download/1?file_format=docx" -OJ
    ```
- **성공 응답**: 파일 다운로드 (사용자가 지정한 파일명으로 저장됨)
- **실패 응답** (문서 없음)
    ```json
    { "message": "해당 문서를 찾을 수 없습니다." }
    ```

### 3. 문서 처리 상태 확인 (GET `/api/v1/status/1`)

- **curl 예시**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/status/1"
    ```
- **성공 응답**
    ```json
    {
      "status": "completed"  // "waiting", "processing", "completed", "failed" 중 하나
    }
    ```
- **실패 응답** (서버 오류)
    ```json
    { "detail": { "message": "상태 확인 중 오류가 발생했습니다." } }
    ```

<br>

## 환경 변수(.env) 예시

```env
# 앱 세팅
APP_NAME=AutoBrief API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 서버
HOST=0.0.0.0
PORT=8000

# 파일 저장 설정
UPLOAD_FOLDER=./uploads
AI_OUTPUT_FOLDER=./ai/outputs

# 허용된 파일 형식
ALLOWED_EXTENSIONS=mpeg

# AI 서비스 설정
AI_SERVICE_URL=http://localhost:8001

# 검색/DB/외부 API 키
SERPER_API_KEY=**********
QDRANT_API_KEY=**********
QDRANT_URL=**********
TAVILY_API_KEY=**********
POLYGON_API_KEY=**********
GNEWS_API_KEY=**********
PINECONE_API_KEY=**********
OPENAI_API_KEY=**********
LANGSMITH_API_KEY=**********