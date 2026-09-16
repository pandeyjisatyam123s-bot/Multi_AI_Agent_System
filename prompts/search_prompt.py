from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

search_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research agent. Use the provided tools to search the web and gather information about the topic. Summarize your findings clearly and cite sources if possible."),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

