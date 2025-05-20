# config.py
from pydantic_settings import BaseSettings
from typing import Set, ClassVar, List
import os
from dotenv import load_dotenv
from enum import Enum

# .env 파일에서 환경 변수 로드
load_dotenv()

class TemplateType(str, Enum):
    """문서 템플릿 유형"""
    LECTURE_NOTE = "lecture_note"    # 강의 노트
    MEETING_MINUTES = "meeting_minutes"  # 회의록
    WARD_ROUND = "ward_round"        # 병동 순회
    REPORT = "report"                # 보고서

class FileFormat(str, Enum):
    """지원하는 파일 형식"""
    DOCX = "docx"  # Word 문서
    PDF = "pdf"    # PDF 문서
    TXT = "txt"    # 일반 텍스트

class Settings(BaseSettings):
    # 앱 설정
    APP_NAME: str = os.getenv("APP_NAME", "AutoBrief API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    API_V1_STR: str = "/api/v1"  # API 버전 접두사
    
    # 서버 설정
    HOST: str = os.getenv("HOST", "0.0.0.0")  # 서버 호스트
    PORT: int = int(os.getenv("PORT", 8000))   # 서버 포트
    
    # 파일 설정
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "./uploads")  # 파일 업로드 경로
    AI_OUTPUT_FOLDER: str = os.getenv("AI_OUTPUT_FOLDER", "./ai/outputs")  # AI 출력 파일 경로
    # 16MB in bytes (16 * 1024 * 1024)
    MAX_CONTENT_LENGTH: int = 16_777_216  # 최대 파일 크기 (16MB)
    # 허용되는 오디오 파일 확장자 (mpeg로 통일)
    ALLOWED_EXTENSIONS: Set[str] = {"mpeg"}
    
    # 템플릿 및 파일 형식
    TEMPLATES: ClassVar[List[str]] = ["lecture_note", "meeting_minutes", "ward_round", "report"]
    FILE_FORMATS: ClassVar[List[str]] = ["docx", "pdf", "txt"]
    
    # AI 서비스 URL (필요시 사용)
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://localhost:8001")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"  # 추가 필드 허용
    }

# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
