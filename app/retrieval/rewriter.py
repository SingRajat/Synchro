from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

parser=StrOutputParser()

List_Parser=RunnableLambda(lambda x: [q.strip() for q in x.split("\n") if q.strip()])

def Rewrite_chain(llm):
    Rewrite_prompt=ChatPromptTemplate.from_messages([
        ("system","""You are a Query Intelligence Engine embedded inside a RAG pipeline.

Your ONLY job is to rewrite a user's raw query into the best possible
search query for a vector database retriever — one that will surface
the most relevant document chunks for the LLM to answer with."""),
         MessagesPlaceholder(variable_name="Message_History"),
         ("user","{input}")
    ])

    rewrite_chain=Rewrite_prompt|llm| parser | List_Parser
    return rewrite_chain
