# download_document.py
from fastapi import APIRouter, HTTPException, Path, Query, Response
from app.config import settings
from app.api.generate_document import latest_filename_state
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

        # AI가 생성한 output_file.{확장자} 파일 경로 확인
        file_path = os.path.join(settings.AI_OUTPUT_FOLDER, f"output_file.{file_format}")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail={"message": "해당 문서를 찾을 수 없습니다."})
        
        # 사용자가 요청한 filename 가져오기 (없으면 기본값)
        user_filename = latest_filename_state.get(1, f"output_file")
        if not user_filename.lower().endswith(f".{file_format}"):
            user_filename = f"{user_filename}.{file_format}"

        # 파일 읽기
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        # 가장 기본적인 Response 사용
        response = Response(content=file_content, media_type=MIME_TYPES.get(file_format, "application/octet-stream"))
        response.headers["Content-Disposition"] = f'attachment; filename="{user_filename}"'
        
        return response

    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail={"message": "파일 처리 중 오류가 발생했습니다."})