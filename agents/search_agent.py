from langchain_core.messages import AIMessage
from prompts.search_prompt import search_prompt
from tools.tavily_search import get_search_tool
try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
except ImportError:
    from langchain_classic.agents import create_tool_calling_agent, AgentExecutor


class SearchAgent:
    def __init__(self, llm):
        self.llm = llm
        tools = [get_search_tool()]
        self.agent = create_tool_calling_agent(llm, tools, search_prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)

    def run(self, state):
        messages = state.get("messages", [])
        response = self.executor.invoke({"messages": messages})
        return {"messages": [AIMessage(content=response["output"], name="Search")]}
