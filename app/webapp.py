import sys
import os
import streamlit as st

# 1. SETUP PATHS
# Get the absolute path to the directory containing 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(current_dir)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 2. UI SETUP
st.set_page_config(page_title="RAG Debugger", layout="centered")
st.title("🌌 Synchro RAG Interface")

# 3. LAZY LOADING LOGIC
# We use a function to load the pipeline so the app doesn't crash on boot.
@st.cache_resource
def get_pipeline():
    try:
        from app.orchestrator.pipeline import execute_chat
        return execute_chat
    except Exception as e:
        st.error(f"Failed to load pipeline: {e}")
        return None

# 4. CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. INTERACTION
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We load the pipeline ONLY when the first message is sent
        pipeline = get_pipeline()
        
        if pipeline:
            with st.spinner("Analyzing..."):
                try:
                    response = pipeline("Streamlit_UI", prompt)
                    answer = response.content
                except Exception as e:
                    answer = f"⚠️ Pipeline Error: {str(e)}"
        else:
            answer = "❌ Pipeline could not be initialized. Check terminal for errors."

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
