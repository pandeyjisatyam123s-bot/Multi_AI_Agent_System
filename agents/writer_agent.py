from langchain_core.messages import AIMessage
from prompts.writer_prompt import writer_prompt

class WriterAgent:
    def __init__(self, llm):
        self.llm = llm
        self.chain = writer_prompt | llm

    def run(self, state):
        messages = state.get("messages", [])
        response = self.chain.invoke({"messages": messages})
        return {
            "messages": [AIMessage(content=response.content, name="Writer")],
            "final_report": response.content
        }
