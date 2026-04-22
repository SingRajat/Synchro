from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import trim_messages

store={}

def get_session_history(session_id: str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=ChatMessageHistory()
    return store[session_id]

def trimmer(messages,llm):
    trim=trim_messages(
        max_tokens=2000,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human"
    )
    
    return trim.invoke(messages)

Recent_window=6
Summary_threshold=600

def Summarize(session_id: str, llm):

    history= store.get