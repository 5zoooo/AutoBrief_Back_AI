# ai/agents/template_structure_agent.py

from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

class TemplateStructureAgent(Runnable):
    def __init__(self, vectorstore: PineconeVectorStore, prompt_path: str, llm=None):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_str = f.read()
        self.vectorstore = vectorstore
        self.prompt_template = PromptTemplate.from_template(template_str)
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.output_parser = StrOutputParser()

    def invoke(self, template_id: str) -> str:
        # 벡터 DB에서 이미지 설명 (type=template) 가져오기
        results = self.vectorstore.similarity_search(template_id, k=1)
        image_description = "\n\n".join([
            doc.page_content for doc in results if doc.metadata.get("type") == "template"
        ])

        prompt_input = {
            "image_description": image_description,
            "template_id": template_id
        }

        chain = self.prompt_template | self.llm | self.output_parser
        return chain.invoke(prompt_input)
