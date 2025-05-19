from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Pinecone as PineconeVectorStore

class FinalReportAgent(Runnable):
    def __init__(self, vectorstore: PineconeVectorStore, prompt_path: str, llm=None):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_str = f.read()
        self.vectorstore = vectorstore
        self.prompt_template = PromptTemplate.from_template(template_str)
        self.llm = llm or ChatOpenAI(temperature=0.2)
        self.output_parser = StrOutputParser()

    def invoke(self, inputs: dict) -> str:
        results = self.vectorstore.similarity_search(inputs["template_id"], k=2)
        example_reference = "\n\n".join([
            doc.page_content for doc in results if doc.metadata.get("type") == "example"
        ])
        prompt_input = {
            "summary_text": inputs["summary_text"],
            "markdown_format": inputs["markdown_format"],
            "template_id": inputs["template_id"],
            "example_reference": example_reference
        }
        chain = self.prompt_template | self.llm | self.output_parser
        return chain.invoke(prompt_input)
