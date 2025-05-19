# download_document.py
from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import FileResponse
from app.config import settings
from app.api.document_state import document_tasks
import os

router = APIRouter(
    prefix=settings.API_V1_STR,
    tags=["documents"]
)

MIME_TYPES = {
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pdf": "application/pdf",
    "txt": "text/plain"
}

@router.get("/download/{document_id}")
async def download_document(
    document_id: int = Path(..., description="다운로드할 문서 ID"),
    file_format: str = Query(..., description="파일 형식 (docx, pdf, txt)")
):
    try:
        # 항상 document_id=1만 허용
        if document_id != 1:
            raise HTTPException(status_code=404, detail={"message": "해당 문서를 찾을 수 없습니다."})

        task = document_tasks.get(1)
        if not task:
            raise HTTPException(status_code=404, detail={"message": "해당 문서를 찾을 수 없습니다."})

        file_path = os.path.join(settings.AI_OUTPUT_FOLDER, task.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail={"message": "해당 문서를 찾을 수 없습니다."})

        content_type = MIME_TYPES.get(file_format, "application/octet-stream")
        headers = {
            "Content-Disposition": f'attachment; filename="{task.filename}"'
        }

        return FileResponse(
            path=file_path,
            filename=task.filename,
            media_type=content_type,
            headers=headers
        )

    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail={"message": "파일 처리 중 오류가 발생했습니다."})