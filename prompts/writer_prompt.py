from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert technical writer. Write a comprehensive report based on the provided research data in the conversation. Format the report nicely using Markdown. If the information is insufficient, state that clearly."),
    MessagesPlaceholder(variable_name="messages"),
])
