# main.py
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.api import generate_document, download_document, check_status

# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.APP_NAME,
    description="오디오 파일로부터 문서를 생성하는 AutoBrief API",
    version=settings.APP_VERSION,
    docs_url="/docs",  # Swagger UI 문서 URL
    redoc_url="/redoc",  # ReDoc 문서 URL
    openapi_url="/openapi.json"  # OpenAPI 스키마 URL
)

# CORS 미들웨어 추가 (개발용으로 모든 도메인 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한하는 것이 좋음
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 필요한 디렉토리 생성 (없는 경우)
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(settings.AI_OUTPUT_FOLDER, exist_ok=True)

# 정적 파일 서빙 설정
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_FOLDER), name="uploads")  # 업로드된 파일 제공
app.mount("/ai-outputs", StaticFiles(directory=settings.AI_OUTPUT_FOLDER), name="ai_outputs")  # AI 출력 파일 제공

# API 라우터 등록
app.include_router(generate_document.router)  # 문서 생성 API
app.include_router(download_document.router)  # 문서 다운로드 API
app.include_router(check_status.router)  # 문서 상태 확인 API

@app.get("/", tags=["Root"])
async def root():
    """API 기본 정보를 반환하는 엔드포인트"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",  # Swagger UI 문서 링크
        "redoc": "/redoc"  # ReDoc 문서 링크
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """헬스 체크 엔드포인트 (로드 밸런서나 모니터링용)"""
    return {"status": "ok"}

# Root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Root endpoint with API information."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }

# This would be used to serve the frontend in production
# @app.get("/{full_path:path}")
# async def serve_frontend(full_path: str):
#     if full_path.startswith("api/"):
#         # Handle API routes
#         raise HTTPException(status_code=404, detail="API route not found")
#     # Serve your frontend's index.html for SPA routing
#     return FileResponse("path/to/your/frontend/build/index.html")