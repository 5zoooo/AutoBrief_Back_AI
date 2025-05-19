import os
import sys

# 1. 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# 2. 에이전트 및 설정 불러오기
from ai.config import config
from ai.agents.summarizer_agent import MeetingSummaryAgent
from ai.agents.markdown_converter_agent import TemplateGeneratorAgent
from ai.agents.report_builder_agent import FinalReportAgent
from langchain_openai import ChatOpenAI  # ✅ 모델 지정용 LLM 추가

# 3. 프롬프트 경로 설정
PROMPT_DIR = os.path.join(config.BASE_DIR, "ai", "prompts")

# 4. LLM 설정 (gpt-4o로 고정)
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# 5. 에이전트 인스턴스 생성 (공통 LLM 주입)
summary_agent = MeetingSummaryAgent(
    prompt_path=os.path.join(PROMPT_DIR, "summarizer_prompt.txt"),
    llm=llm
)
template_agent = TemplateGeneratorAgent(
    vectorstore=config.vectorstore,
    prompt_path=os.path.join(PROMPT_DIR, "markdown_format_prompt.txt"),
    llm=llm
)
final_report_agent = FinalReportAgent(
    vectorstore=config.vectorstore,
    prompt_path=os.path.join(PROMPT_DIR, "report_building_prompt.txt"),
    llm=llm
)

# 6. 입력 파일 경로
TEXT_PATH = os.path.join(config.BASE_DIR, "ai","uploads", "audio_text.txt")
TEMPLATE_ID = "basic_tem"

def run_pipeline():
    # 1. 텍스트 불러오기
    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("\n📝 [1] 회의 요약 중...")
    summary = summary_agent.invoke(raw_text)

    print("\n📐 [2] 템플릿 구조 생성 중...")
    markdown_format = template_agent.invoke(template_id=TEMPLATE_ID)

    print("\n📄 [3] 최종 보고서 생성 중...")
    final_report = final_report_agent.invoke({
        "summary_text": summary,
        "markdown_format": markdown_format,
        "template_id": TEMPLATE_ID
    })

    return final_report

if __name__ == "__main__":
    result = run_pipeline()

    print("\n✅ 최종 회의록 결과:\n")
    print(result)
    