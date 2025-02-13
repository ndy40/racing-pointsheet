from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel


class VertexAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = None
        self.llm = ChatVertexAI(
            model_name="gemini-2.0-flash-001",
            temperature=0,
            client_options={"api_key": "AIzaSyCQ2glxUjVNTd3FzrpR0v79pIj8UXeNd3w"},
            project="logical-veld-450313-k4",
        )

    def create_system_prompt(self, *messages, response_model: BaseModel = None):
        def system_prompt(context):
            template = ChatPromptTemplate.from_messages(messages)

            parser = PydanticOutputParser(pydantic_object=response_model)

            if response_model:
                # chain = template | self.llm.with_structured_output(schema=response_model.model_json_schema())
                chain = template | self.llm | parser
            else:
                chain = template | self.llm

            return chain.invoke(context)

        return system_prompt
