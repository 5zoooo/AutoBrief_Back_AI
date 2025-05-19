from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Pinecone as PineconeVectorStore

class FinalDocumentAgent(Runnable):
    def __init__(self, vectorstore: PineconeVectorStore, prompt_path: str, llm=None):
        self.vectorstore = vectorstore
        self.prompt_template = self._load_prompt(prompt_path)
        self.llm = llm or ChatOpenAI(temperature=0.3)
        self.output_parser = StrOutputParser()

    def _load_prompt(self, path: str) -> PromptTemplate:
        with open(path, "r", encoding="utf-8") as f:
            return PromptTemplate.from_template(f.read())

    def invoke(self, inputs: dict) -> str:
        # inputs = { "summary_text": str, "markdown_format": str, "template_id": str }

        # example 문서 검색
        results = self.vectorstore.similarity_search(inputs["template_id"], k=3)
        examples = "\n\n".join([
            doc.page_content for doc in results if doc.metadata.get("type") == "example"
        ])

        prompt_input = {
            "summary_text": inputs["summary_text"],
            "markdown_format": inputs["markdown_format"],
            "template_id": inputs["template_id"],
            "example_reference": examples
        }

        chain = self.prompt_template | self.llm | self.output_parser
        return chain.invoke(prompt_input)
