from langchain_core.runnables import Runnable
from weasyprint import HTML
import os
import re

class TemplatePdfWriterAgent(Runnable):
    def __init__(self, output_dir: str = "./outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def invoke(self, inputs: dict) -> str:
        # ✅ summary_text만 사용하여 PDF 생성
        summary_text = inputs["summary_text"]

        # 🔍 ```html ... ``` 코드 블록이 있으면 그 내부만 추출
        match = re.search(r"```html\s*(.*?)```", summary_text, re.DOTALL)
        html_content = match.group(1).strip() if match else summary_text.strip()

        # ✅ HTML 형식이 아닐 경우 <div>로 감싸기
        if not html_content.startswith("<"):
            html_content = f"<div>{html_content}</div>"

        # 📝 PDF 저장 경로 정의
        output_path = os.path.join(self.output_dir, "output_file.pdf")

        # 🖨️ PDF 생성
        HTML(string=html_content).write_pdf(output_path)

        return output_path
