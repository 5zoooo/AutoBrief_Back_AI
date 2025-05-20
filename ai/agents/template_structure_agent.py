# ai/agents/template_structure_agent_v2.py

import base64
import os
from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from openai import OpenAI

class TemplateStructureAgent(Runnable):
    def __init__(self, vectorstore: PineconeVectorStore, vision_client: OpenAI, prompt_path: str, llm=None):
        self.vectorstore = vectorstore
        self.vision_client = vision_client
        self.llm = llm or ChatOpenAI(temperature=0.2, model="gpt-4o")

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = PromptTemplate.from_template(f.read())

        self.output_parser = StrOutputParser()

    def describe_image(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response = self.vision_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 이미지를 문서 템플릿의 시각적 구조로 자세히 설명해줘."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ],
                }
            ],
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()

    def invoke(self, inputs: dict) -> str:
        template_id = inputs["template_id"]
        image_path = inputs["template_image_path"]

        # 1. 벡터DB에서 템플릿 설명 검색
        docs = self.vectorstore.similarity_search(template_id, k=3)
        reference = "\n\n".join([doc.page_content for doc in docs if doc.metadata.get("type") == "template"])

        # 2. Vision을 통해 이미지 설명 추출
        vision_description = self.describe_image(image_path)

        # 3. 프롬프트 입력 구성
        prompt_input = {
            "template_reference": reference,
            "image_description": vision_description,
            "template_id": template_id
        }

        chain = self.prompt_template | self.llm | self.output_parser
        return chain.invoke(prompt_input)
