from app.llm.generator import Get_LLM
from app.llm.prompt_builder import Prompt_builder
from app.retrieval.vector_store import RAG_Logic
from app.retrieval.retriever import Retriever
from app.retrieval.rewriter import Rewrite_chain
from app.memory.chat_history import get_session_history
from langchain_core.runnables import RunnableWithMessageHistory

llm=Get_LLM()
Vector_db=RAG_Logic().builder("AI Career Platform Research Plan.pdf")
retrieve=Retriever(Vector_db)
R_Chain=Rewrite_chain(llm)

Prompt_chain=Prompt_builder(llm,retrieve,R_Chain)

Msg_History=RunnableWithMessageHistory(
    Prompt_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="Message_History"
)




