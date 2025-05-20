from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class TemplateSummarizerAgent(Runnable):
    def __init__(self, prompt_path: str, llm=None):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_str = f.read()
        self.prompt_template = PromptTemplate.from_template(template_str)
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.output_parser = StrOutputParser()

    def invoke(self, inputs: dict) -> str:
        """
        inputs: {
            "raw_text": str,
            "template_structure": str
        }
        """
        prompt_input = {
            "raw_text": inputs["raw_text"],
            "template_structure": inputs["template_structure"]
        }

        chain = self.prompt_template | self.llm | self.output_parser
        return chain.invoke(prompt_input)
