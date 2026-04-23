from operator import itemgetter
from app.retrieval.retriever import Retriever
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def Prompt_builder(llm,retriever,rewrite_chain):
    prompt=ChatPromptTemplate.from_messages([
        ("system","""You are a precise and helpful Knowledge Assistant operating in a RAG pipeline.
Your job is to answer the user's question using ONLY the provided context.
- Provide maximum signal per token: zero filler, zero redundancy.
- If the context does not contain the answer, say "I don't know based on the context." Do not hallucinate.
- Use a clean, structured format (bullet points if applicable)."""),
             MessagesPlaceholder(variable_name="Message_History"),
             ("user","<context>{context}</context> Question:{input}")
    ])

    prompt_chain = (
        RunnablePassthrough.assign(
            context=(RunnablePassthrough() | rewrite_chain | retriever | format_docs)
        )
        | prompt
        | llm
    )
    
    return prompt_chain