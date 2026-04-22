from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

def Rewrite_chain(llm):
    Rewrite_prompt=ChatPromptTemplate.from_messages([
        ("system","""You are a Query Intelligence Engine embedded inside a RAG pipeline.

Your ONLY job is to rewrite a user's raw query into the best possible
search query for a vector database retriever — one that will surface
the most relevant document chunks for the LLM to answer with."""),
         MessagesPlaceholder(variable_name="Message_History"),
         ("user","{input}")
    ])

    rewrite_chain=Rewrite_prompt|llm
    return rewrite_chain
