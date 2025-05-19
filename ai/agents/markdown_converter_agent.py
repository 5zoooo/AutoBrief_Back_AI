from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
import os

class TemplateToMarkdownAgent(Runnable):
    def __init__(self, vectorstore: PineconeVectorStore, prompt_path: str, llm=None):
        self.vectorstore = vectorstore
        self.prompt_template = self._load_prompt(prompt_path)
        self.llm = llm or ChatOpenAI(temperature=0.2)
        self.output_parser = StrOutputParser()

    def _load_prompt(self, path: str) -> PromptTemplate:
        with open(path, "r", encoding="utf-8") as f:
            template_str = f.read()
        return PromptTemplate.from_template(template_str)

    def invoke(self, template_id: str) -> str:
        # 1. 템플릿 문서 검색
        results = self.vectorstore.similarity_search(template_id, k=3)
        template_docs = "\n\n".join([
            doc.page_content for doc in results if doc.metadata.get("type") == "template"
        ])

        # 2. 프롬프트 입력 구성
        prompt_input = {
            "template_reference": template_docs,
             "template_id": template_id 
        }

        # 3. LLM 호출
        chain = self.prompt_template | self.llm | self.output_parser
        return chain.invoke(prompt_input)

