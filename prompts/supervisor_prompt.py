from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

supervisor_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a supervisor tasked with managing a research workflow.
Given a user request, decide which agent to invoke next.
- Use 'Search' to gather information.
- Use 'Writer' to compile the gathered information into a final report.
- Use 'FINISH' when the report is complete.
"""),
    MessagesPlaceholder(variable_name="messages"),
    ("user", "Given the conversation above, who should act next? Respond with ONLY ONE WORD: 'Search', 'Writer', or 'FINISH'.")
])

