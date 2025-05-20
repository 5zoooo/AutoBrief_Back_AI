# generate_document.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
from app.config import settings
from app.dependencies.file_utils import save_uploaded_file, get_file_extension
from app.api.document_state import document_tasks, document_state
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

latest_filename_state = {}

@router.post("/generate-document", status_code=status.HTTP_201_CREATED)
async def generate_document(
    file: UploadFile = File(...),
    template: str = Form(...),
    file_format: str = Form(...),
    filename: str = Form(...)
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

        # 파일 확장자 확인
        file_extension = get_file_extension(file.filename)
        if file_extension != "mpeg":
            raise HTTPException(status_code=400, detail={"message": "mpeg 파일만 지원합니다."})
            
        # 문서 처리 상태 초기화 - 처리 시작
        document_state.start_processing(filename, file_format)
        
        # 파일 저장 - 항상 mpeg로 저장
        fixed_filename = "audio_file.mpeg"
        saved_file_path = await save_uploaded_file(file, settings.UPLOAD_FOLDER, fixed_filename)

        # 요약문 생성(임시)
        summary = f"{template} 템플릿으로 생성된 요약본입니다."

        # 항상 document_id=1로 저장 (덮어쓰기)
        doc_req = DocumentRequest(file, template, file_format, filename, summary)
        document_tasks[1] = doc_req
        latest_filename_state[1] = filename
        
        # 실제 처리가 완료되면 상태를 변경해야 함 (실제 AI 처리가 완료되면 complete_processing 호출)
        # 이 예제에서는 실제 처리가 없으므로 임시로 완료 상태로 설정
        # 실제 구현에서는 비동기 처리가 완료된 후에 complete_processing을 호출해야 함
        document_state.complete_processing()

        return {
            "download_url": f"/api/v1/download/1?file_format={file_format}"
        }

    except HTTPException as he:
        # HTTP 예외가 발생하면 처리 실패로 상태 업데이트
        document_state.fail_processing(str(he.detail))
        raise he
    except Exception as e:
        # 기타 예외가 발생하면 처리 실패로 상태 업데이트
        error_message = f"파일 처리 중 오류가 발생했습니다: {str(e)}"
        document_state.fail_processing(error_message)
        raise HTTPException(status_code=500, detail={"message": error_message})