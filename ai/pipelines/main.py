import sys
import os

# 상위 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ai.config import config
from ai.pipelines.audio_to_text import audio_file_to_text

def run_pipeline(audio_path: str, template_id: str = "basic") -> str:
    print("🎧 [1] 음성 → 텍스트 변환 중...")
    raw_text = audio_file_to_text(audio_path)

    print("📝 [2] 회의 요약 중...")
    summary = config.summary_agent.invoke(raw_text)

    print("🧱 [3] 마크다운 양식 변환 중...")
    markdown = config.markdown_agent.invoke("basic_tem")

    print("📄 [4] 최종 회의록 생성 중...")
    final_report = config.final_doc_agent.invoke({
        "summary_text": summary,
        "markdown_format": markdown,
        "template_id": 'basic_ex'
    })

    return final_report

if __name__ == "__main__":
    audio_path = os.path.join(config.UPLOAD_DIR, "회의 음성.mp3")
    report = run_pipeline(audio_path, template_id="basic")

    print("\n✅ 최종 회의록 결과:\n")
    print(report)
