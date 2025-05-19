# generate_document.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
from app.config import settings
from app.dependencies.file_utils import save_uploaded_file, get_file_extension
from app.api.document_state import document_tasks
import os

router = APIRouter(
    prefix=settings.API_V1_STR,
    tags=["documents"],
    responses={404: {"description": "요청한 리소스를 찾을 수 없습니다"}},
)

class DocumentRequest:
    def __init__(self, file: UploadFile, template: str, file_format: str, filename: str, summary: str):
        self.file = file
        self.template = template
        self.file_format = file_format.lower()
        self.filename = filename
        self.summary = summary

@router.post("/generate-document", status_code=status.HTTP_201_CREATED)
async def generate_document(
    file: UploadFile = File(...),
    template: str = Form(...),
    file_format: str = Form(...),
    filename: Optional[str] = Form(None)
):
    try:
        if template not in settings.TEMPLATES:
            raise HTTPException(status_code=400, detail={"message": f"지원하지 않는 템플릿입니다. {settings.TEMPLATES}"})
        if file_format not in settings.FILE_FORMATS:
            raise HTTPException(status_code=400, detail={"message": f"지원하지 않는 파일 형식입니다. {settings.FILE_FORMATS}"})

        # 파일명 처리
        if not filename:
            filename = "document_1"
        if not filename.lower().endswith(f".{file_format}"):
            filename = f"{filename}.{file_format}"

        # 파일 저장
        file_extension = file.filename.split('.')[-1].lower()
        fixed_filename = f"audio_file.{file_extension}"
        saved_file_path = await save_uploaded_file(file, settings.UPLOAD_FOLDER, fixed_filename)

        # 요약문 생성(임시)
        summary = f"{template} 템플릿으로 생성된 요약본입니다."

        # 항상 document_id=1로 저장 (덮어쓰기)
        doc_req = DocumentRequest(file, template, file_format, filename, summary)
        document_tasks[1] = doc_req

        download_url = f"{settings.API_V1_STR}/download/1?file_format={file_format}"

        return {
            "summary": summary,
            "filename": filename.replace(f".{file_format}", ""),
            "download_url": download_url
        }

    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail={"message": "파일 처리 중 오류가 발생했습니다."})