from langchain_core.runnables import Runnable
from weasyprint import HTML
import os

class TemplatePdfWriterAgent(Runnable):
    def __init__(self, output_dir: str = "./outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def invoke(self, inputs: dict) -> str:
        # ✅ summary_text만 사용하여 PDF 생성
        summary_text = inputs["summary_text"]

        # HTML 형식이 아닐 경우 <div>로 감싸기
        summary_html = (
            f"<div>{summary_text.strip()}</div>"
            if not summary_text.strip().startswith("<")
            else summary_text.strip()
        )

        # PDF 파일 경로 정의
        output_path = os.path.join(self.output_dir, "generated_template.pdf")

        # PDF 생성
        HTML(string=summary_html).write_pdf(output_path)

        return output_path
