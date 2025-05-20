# check_status.py
from fastapi import APIRouter, HTTPException, Path
from app.config import settings
from app.api.document_state import document_state, ProcessingStatus
import os

router = APIRouter(
    prefix=settings.API_V1_STR,
    tags=["documents"]
)

@router.get("/status/1")
async def check_document_status():
    """
    문서 처리 상태를 확인합니다.
    
    Returns:
        dict: 문서 처리 상태 정보
    """
    try:
        # 문서 상태 객체에서 상태 정보 가져오기
        status_info = document_state.get_status()
        
        # 상태가 COMPLETED로 설정되어 있더라도 실제 파일이 존재하는지 확인
        if status_info["status"] == ProcessingStatus.COMPLETED:
            output_file_path = os.path.join(settings.AI_OUTPUT_FOLDER, "output_file.docx")
            if not os.path.exists(output_file_path):
                # 파일이 존재하지 않으면 상태를 PROCESSING으로 변경
                document_state.status = ProcessingStatus.PROCESSING
                status_info["status"] = ProcessingStatus.PROCESSING
        
        # API 응답 형식에 맞게 변환
        return {"status": status_info["status"]}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"상태 확인 중 오류가 발생했습니다: {str(e)}"})

