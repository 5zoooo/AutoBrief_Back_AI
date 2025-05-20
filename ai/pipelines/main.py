import os
import sys
import json
import re

# 1. 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# 2. 에이전트 및 설정
from ai.config import config
from ai.agents.template_structure_agent import TemplateStructureAgent
from ai.agents.template_summarizer_agent import TemplateSummarizerAgent
from ai.agents.word_export_agent import WordExporterAgent
from langchain_openai import ChatOpenAI

# 3. 설정
TEMPLATE_ID = "basic_tem"
TEXT_PATH = os.path.join(config.BASE_DIR, "ai", "uploads", "audio_text.txt")
OUTPUT_PATH = os.path.join(config.BASE_DIR, "ai", "outputs", "final_report.docx")

# 4. 프롬프트 경로
structure_prompt_path = os.path.join(config.PROMPT_DIR, "template_structure_prompt.txt")
summarizer_prompt_path = os.path.join(config.PROMPT_DIR, "summarizer_by_structure_prompt.txt")

# 5. LLM 정의
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# 6. 에이전트 인스턴스 초기화
structure_agent = TemplateStructureAgent(
    vectorstore=config.vectorstore,
    prompt_path=structure_prompt_path,
    llm=llm
)

summarizer_agent = TemplateSummarizerAgent(
    prompt_path=summarizer_prompt_path,
    llm=llm
)

exporter_agent = WordExporterAgent(output_path=OUTPUT_PATH)

# 🔧 GPT 응답 내 코드블럭(````json`) 제거 함수
def extract_json_block(text: str) -> str:
    match = re.search(r"```json\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def run_pipeline():
    # 1. 텍스트 불러오기
    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("\n🧱 [1] 템플릿 구조 분석 중...")
    template_structure = structure_agent.invoke(TEMPLATE_ID)
    print("[결과] 템플릿 구조 분석 결과:\n", template_structure[:500], "\n")

    print("📝 [2] 텍스트 요약 및 템플릿 구조 반영 중...")
    filled_structure = summarizer_agent.invoke({
        "template_structure": template_structure,
        "raw_text": raw_text
    })
    print("[결과] 요약 + 구조 반영 결과:\n", filled_structure[:500], "\n")

    print("📄 [3] Word 문서로 내보내는 중...")
    try:
        cleaned_json = extract_json_block(filled_structure)
        filled_dict = json.loads(cleaned_json)
    except Exception as e:
        print("[❌ 오류] JSON 파싱 실패:", e)
        print("[내용]:\n", filled_structure[:500])
        return

    file_path = exporter_agent.export(filled_dict)
    print(f"\n✅ 최종 보고서 생성 완료: {file_path}")
    return file_path

if __name__ == "__main__":
    run_pipeline()
