# create_test_file.py
from pathlib import Path
import os

def create_test_file():
    # 프로젝트 루트 디렉토리 기준으로 경로 설정
    project_root = Path(__file__).parent.parent.parent
    ai_output_dir = project_root / "ai" / "outputs"
    
    # 디렉토리 생성
    ai_output_dir.mkdir(parents=True, exist_ok=True)
    
    # 테스트용 더미 파일 생성
    test_file = ai_output_dir / "test_document.docx"
    test_file.write_text("This is a test document content")
    
    print(f"테스트 파일이 생성되었습니다: {test_file.absolute()}")
    return str(test_file.absolute())

if __name__ == "__main__":
    create_test_file()