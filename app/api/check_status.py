# check_status.py
from fastapi import APIRouter, HTTPException, Path
from app.config import settings
from app.api.document_state import document_state
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
        
        # API 응답 형식에 맞게 변환
        return {"status": status_info["status"]}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"상태 확인 중 오류가 발생했습니다: {str(e)}"})

