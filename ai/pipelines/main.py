import os
import sys
import re

# 1. 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# 2. 에이전트 및 설정
from ai.config import config
from ai.config import template_image_path_map, vision_client
from ai.agents.template_structure_agent import TemplateStructureAgent
from ai.agents.template_summarizer_agent import TemplateSummarizerAgent
from ai.agents.template_pdf_writer_agent import TemplatePdfWriterAgent  # ✅ PDF용 에이전트로 변경
from langchain_openai import ChatOpenAI

# 3. 설정
TEMPLATE_ID = "basic_tem"
TEXT_PATH = os.path.join(config.BASE_DIR, "ai", "uploads", "audio_text.txt")

# 4. 프롬프트 경로
structure_prompt_path = os.path.join(config.PROMPT_DIR, "template_structure_prompt.txt")
summarizer_prompt_path = os.path.join(config.PROMPT_DIR, "summarizer_by_structure_prompt.txt")

# 5. LLM 정의
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# 6. 에이전트 인스턴스 초기화
structure_agent = TemplateStructureAgent(
    vectorstore=config.vectorstore,
    vision_client=config.vision_client,
    prompt_path=structure_prompt_path,
    llm=llm
)

summarizer_agent = TemplateSummarizerAgent(
    prompt_path=summarizer_prompt_path,
    llm=llm
)

pdf_writer_agent = TemplatePdfWriterAgent(  # ✅ docx → pdf
    output_dir=os.path.join(config.BASE_DIR, "ai", "outputs")
)

def run_pipeline():
    # 1. 텍스트 불러오기
    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("\n🧱 [1] 템플릿 구조 분석 중...")
    template_structure = structure_agent.invoke({
        "template_id": TEMPLATE_ID,
        "template_image_path": config.template_image_path_map[TEMPLATE_ID]
    })
    print("[결과] 템플릿 구조 분석 결과:\n", template_structure[:500], "\n")

    print("📝 [2] 텍스트 요약 및 템플릿 구조 반영 중...")
    summary_text = summarizer_agent.invoke({
        "template_structure": template_structure,
        "raw_text": raw_text
    })
    print("[결과] 요약 결과:\n", summary_text[:500], "\n")

    print("📄 [3] PDF 문서로 내보내는 중...")
    file_path = pdf_writer_agent.invoke({
        "template_structure": template_structure,
        "summary_text": summary_text
    })

    print(f"\n✅ 최종 PDF 보고서 생성 완료: {file_path}")
    return file_path

if __name__ == "__main__":
    run_pipeline()
