from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import trim_messages, SystemMessage

store={}
summary_store={}

def get_session_history(session_id: str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=ChatMessageHistory()
    return store[session_id]

def get_user_summary(session_id:str):
    if session_id not in summary_store: return ""
    return summary_store[session_id]

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
    history = store.get(session_id)
    if history is None: return

    messages = history.messages
    if len(messages) <= Recent_window: return

    existing_summary = get_user_summary(session_id)
    
    old_messages = messages[:-2]
    recent_messages = messages[-2:]

    formatted_old = "\n".join([f"{msg.type}: {msg.content}" for msg in old_messages])
    
    prompt = SystemMessage(
        content=f"Combine existing summary: '{existing_summary}' and new messages: '{formatted_old}' into a single concise paragraph of facts."
    )
    
    response = llm.invoke([prompt])
    summary_store[session_id] = response.content.strip()

    history.clear()
    history.add_messages(recent_messages)
