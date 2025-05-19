import os
from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class MeetingSummaryAgent(Runnable):
    def __init__(self, prompt_path: str, llm=None):
        self.prompt_template = self._load_prompt(prompt_path)
        self.llm = llm or ChatOpenAI(temperature=0.3)
        self.output_parser = StrOutputParser()

    def _load_prompt(self, path: str) -> PromptTemplate:
        with open(path, "r", encoding="utf-8") as f:
            template_str = f.read()
        return PromptTemplate.from_template(template_str)

    def invoke(self, input_text: str) -> str:
        prompt_input = {"raw_text": input_text}
        chain = self.prompt_template | self.llm | self.output_parser
        return chain.invoke(prompt_input)
