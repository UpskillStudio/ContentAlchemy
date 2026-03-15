import sys
from pathlib import Path

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from src.web_app.components.sidebar import render_sidebar
from src.web_app.components.chat import render_chat_history, render_user_message, render_assistant_response
from src.web_app.components.content_preview import render_content_preview

st.set_page_config(
    page_title="ContentAlchemy",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "last_state" not in st.session_state:
    st.session_state["last_state"] = {}
if "thread_id" not in st.session_state:
    import uuid
    st.session_state["thread_id"] = str(uuid.uuid4())
if "example_prompt" not in st.session_state:
    st.session_state["example_prompt"] = None

# --- Sidebar ---
config = render_sidebar()

# --- Main Layout ---
st.title("⚗️ ContentAlchemy")
st.caption("Multi-Agent AI Content Marketing Assistant — powered by Claude Sonnet 4.6 + LangGraph")

col_chat, col_preview = st.columns([3, 2])

with col_chat:
    render_chat_history(st.session_state["messages"])

    # Handle sidebar example prompt injection
    example = st.session_state.pop("example_prompt", None)
    prompt = st.chat_input("Ask me to research, write a blog, LinkedIn post, create an image, or build a strategy...") or example

    if prompt:
        render_user_message(prompt)
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            try:
                from src.core.workflow import app

                initial_state = {
                    "messages": st.session_state["messages"],
                    "route": "",
                    "topic": "",
                    "audience": config["audience"],
                    "tone": config["tone"],
                    "research_data": "",
                    "content_output": "",
                    "image_url": None,
                    "seo_metadata": {},
                    "quality_score": {},
                    "error": None,
                }

                config_langgraph = {"configurable": {"thread_id": st.session_state["thread_id"]}}
                result = app.invoke(initial_state, config=config_langgraph)

                st.session_state["last_state"] = result
                render_assistant_response(result)

                assistant_content = result.get("content_output", "")
                if result.get("image_url"):
                    assistant_content += f"\n\n![Generated Image]({result['image_url']})"

                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": assistant_content,
                })

            except Exception as e:
                st.error(f"Workflow error: {str(e)}")
                st.info("Make sure your `.env` file has valid API keys set.")

with col_preview:
    last_state = st.session_state.get("last_state", {})
    if last_state:
        render_content_preview(last_state)
    else:
        st.info(
            "**Welcome to ContentAlchemy!**\n\n"
            "I can help you:\n"
            "- 🔍 **Research** any topic in depth\n"
            "- ✍️ **Write SEO blogs** with keyword optimization\n"
            "- 💼 **Create LinkedIn posts** with hashtag strategy\n"
            "- 🎨 **Generate images** with DALL-E 3\n"
            "- 📋 **Build content strategies** with 4-week calendars\n\n"
            "Start by typing a request in the chat!"
        )
