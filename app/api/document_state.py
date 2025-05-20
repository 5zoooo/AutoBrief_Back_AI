# app/api/document_state.py
from enum import Enum
from datetime import datetime
from typing import Dict, Optional, Any

class ProcessingStatus(str, Enum):
    """문서 처리 상태를 나타내는 열거형"""
    WAITING = "waiting"     # 처리 대기 중
    PROCESSING = "processing"  # 처리 중
    COMPLETED = "completed"   # 처리 완료
    FAILED = "failed"      # 처리 실패

class DocumentState:
    """문서 처리 상태를 관리하는 클래스"""
    def __init__(self):
        self.status: ProcessingStatus = ProcessingStatus.WAITING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self.filename: Optional[str] = None
        self.file_format: Optional[str] = None
        
    def start_processing(self, filename: str, file_format: str) -> None:
        """문서 처리 시작"""
        self.status = ProcessingStatus.PROCESSING
        self.start_time = datetime.now()
        self.filename = filename
        self.file_format = file_format
        self.end_time = None
        self.error_message = None
        
    def complete_processing(self) -> None:
        """문서 처리 완료"""
        self.status = ProcessingStatus.COMPLETED
        self.end_time = datetime.now()
        
    def fail_processing(self, error_message: str) -> None:
        """문서 처리 실패"""
        self.status = ProcessingStatus.FAILED
        self.end_time = datetime.now()
        self.error_message = error_message
        
    def get_status(self) -> Dict[str, Any]:
        """현재 상태 정보 반환"""
        response = {"status": self.status}
        
        # 에러 메시지가 있으면 포함
        if self.error_message:
            response["error"] = self.error_message
            
        return response

# 문서 ID를 키로 하는 문서 상태 딕셔너리 (현재는 단일 문서만 지원하므로 ID는 항상 1)
document_tasks = {}

# 문서 상태 객체 (싱글톤)
document_state = DocumentState()