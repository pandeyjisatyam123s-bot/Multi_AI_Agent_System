from langchain_core.messages import AIMessage
from prompts.supervisor_prompt import supervisor_prompt

class SupervisorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.chain = supervisor_prompt | llm
        
    def run(self, state):
        messages = state.get("messages", [])
        response = self.chain.invoke({"messages": messages})
        raw_text = response.content.strip()

        if "Search" in raw_text:
            next_agent = "Search"
        elif "Writer" in raw_text:
            next_agent = "Writer"
        elif "FINISH" in raw_text or "finish" in raw_text.lower():
            next_agent = "FINISH"
        else:
            has_search = any(getattr(m, "name", "") == "Search" for m in messages)
            has_writer = any(getattr(m, "name", "") == "Writer" for m in messages)
            if not has_search:
                next_agent = "Search"
            elif not has_writer:
                next_agent = "Writer"
            else:
                next_agent = "FINISH"

        return {"next": next_agent}

