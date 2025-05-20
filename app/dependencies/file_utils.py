# file_utils.py
import os
import shutil
import uuid
from typing import Optional, Tuple

from fastapi import UploadFile, HTTPException, status
from app.config import settings

def get_file_extension(filename: str) -> str:
    """파일 확장자를 소문자로 추출하여 반환합니다."""
    return os.path.splitext(filename)[1][1:].lower()

def is_allowed_file(filename: str) -> bool:
    """파일이 허용된 확장자를 가졌는지 확인합니다."""
    return get_file_extension(filename) in settings.ALLOWED_EXTENSIONS

async def save_uploaded_file(upload_file: UploadFile, upload_dir: str, fixed_filename: str = None) -> str:
    """
    업로드된 파일을 지정된 디렉토리에 저장합니다.
    fixed_filename이 주어지면 해당 이름으로 저장(덮어쓰기), 아니면 uuid로 저장
    """
    try:
        # 업로드 디렉토리가 없으면 생성
        os.makedirs(upload_dir, exist_ok=True)
        
        file_extension = get_file_extension(upload_file.filename)
        if not file_extension:
            file_extension = ""  # 확장자가 없는 경우 빈 문자열 사용

        if fixed_filename:
            file_path = os.path.join(upload_dir, fixed_filename)
        else:
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
        
        # 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        return file_path
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"파일을 저장하는 중 오류가 발생했습니다: {str(e)}"
        )

def delete_file(file_path: str) -> bool:
    """
    파일이 존재하는 경우 삭제합니다.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"파일을 삭제하는 중 오류가 발생했습니다: {str(e)}"
        )

def get_mime_type(file_format: str) -> str:
    """
    파일 형식에 해당하는 MIME 타입을 반환합니다.
    """
    mime_types = {
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'pdf': 'application/pdf',
        'txt': 'text/plain',
        'mp3': 'audio/mpeg',
        'm4a': 'audio/mp4',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg'
    }
    return mime_types.get(file_format.lower(), 'application/octet-stream')

def get_file_info(file_path: str) -> Tuple[str, int]:
    """Get file information including MIME type and size."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    mime_type = get_mime_type(get_file_extension(file_path))
    file_size = os.path.getsize(file_path)
    return mime_type, file_size