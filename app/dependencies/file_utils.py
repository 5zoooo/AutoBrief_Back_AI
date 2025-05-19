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


async def save_uploaded_file(upload_file: UploadFile, upload_dir: str) -> str:
    """
    업로드된 파일을 지정된 디렉토리에 고유한 파일명으로 저장합니다.
    
    매개변수:
        upload_file: 업로드된 파일 객체
        upload_dir: 파일을 저장할 디렉토리 경로
        
    반환값:
        str: 저장된 파일의 전체 경로
        
    예외:
        HTTPException: 허용되지 않는 파일 형식이거나 파일 저장 중 오류가 발생한 경우
    """
    try:
        # 업로드 디렉토리가 없으면 생성
        os.makedirs(upload_dir, exist_ok=True)
        
        # 고유한 파일명 생성
        file_extension = get_file_extension(upload_file.filename)
        if not file_extension:
            file_extension = ""  # 확장자가 없는 경우 빈 문자열 사용
            
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
    finally:
        # 파일 포인터 초기화
        await upload_file.seek(0)


def delete_file(file_path: str) -> bool:
    """
    파일이 존재하는 경우 삭제합니다.
    
    매개변수:
        file_path: 삭제할 파일의 경로
        
    반환값:
        bool: 파일이 삭제되면 True, 파일이 존재하지 않으면 False
        
    예외:
        HTTPException: 파일 삭제 중 오류가 발생한 경우
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
    
    Args:
        file_format: File format (docx, pdf, txt, etc.)
        
    Returns:
        str: Corresponding MIME type
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


def get_file_info(file_path: str) -> Tuple[str, str]:
    """Get file information including MIME type and size."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    mime_type = get_mime_type(file_path)
    file_size = os.path.getsize(file_path)
    
    return mime_type, file_size
