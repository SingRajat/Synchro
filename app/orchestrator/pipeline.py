from app.llm.generator import Get_LLM
from app.llm.prompt_builder import Prompt_builder
from app.retrieval.vector_store import RAG_Logic
from app.retrieval.retriever import Retriever
from app.retrieval.rewriter import Rewrite_chain
from app.memory.chat_history import get_session_history, get_user_summary, Summarize
from langchain_core.runnables import RunnableWithMessageHistory

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_path = os.path.join(BASE_DIR, "AI Career Platform Research Plan.pdf")

llm=Get_LLM()
Vector_db,bm25_retriever=RAG_Logic().builder(pdf_path)
retrieve=Retriever(Vector_db,bm25_retriever)
R_Chain=Rewrite_chain(llm)

Prompt_chain=Prompt_builder(llm,retrieve,R_Chain)

Msg_History=RunnableWithMessageHistory(
    Prompt_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="Message_History"
)

def execute_chat(session_id: str, user_input: str):
    current_summary = get_user_summary(session_id)
    
    response = Msg_History.invoke(
        {"input": user_input, "user_summary": current_summary},
        config={"configurable": {"session_id": session_id}}
    )
    
    Summarize(session_id, llm)
    return response
