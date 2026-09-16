from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import Tool

def safe_search(query: str) -> str:
    try:
        ddg_search = DuckDuckGoSearchResults()
        return ddg_search.run(query)
    except Exception as e:
        return f"Search error for '{query}': {str(e)}"

def get_search_tool() -> Tool:
    return Tool(
        name="web_search",
        description="Search the web for information on a topic.",
        func=safe_search
    )

