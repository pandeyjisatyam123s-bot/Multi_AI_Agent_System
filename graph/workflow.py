from langgraph.graph import StateGraph, END
from .state import AgentState
from agents import SupervisorAgent, SearchAgent, WriterAgent
from llm.provider import get_llm

def route_next(state):
    next_agent = state.get("next", "FINISH")
    if next_agent == "FINISH":
        return END
    return next_agent

def create_workflow(provider: str = None, model_name: str = None):
    llm = get_llm(provider=provider, model_name=model_name)

    
    supervisor = SupervisorAgent(llm)
    search_agent = SearchAgent(llm)
    writer_agent = WriterAgent(llm)

    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("Supervisor", supervisor.run)
    workflow.add_node("Search", search_agent.run)
    workflow.add_node("Writer", writer_agent.run)
    
    # Add edges
    # Workers always report back to supervisor
    workflow.add_edge("Search", "Supervisor")
    workflow.add_edge("Writer", "Supervisor")
    
    # Supervisor decides who is next
    workflow.add_conditional_edges(
        "Supervisor",
        route_next,
        {"Search": "Search", "Writer": "Writer", END: END}
    )
    
    # Set entry point
    workflow.set_entry_point("Supervisor")
    
    return workflow.compile()
