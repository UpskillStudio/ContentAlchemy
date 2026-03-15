import streamlit as st


def render_sidebar() -> dict:
    with st.sidebar:
        st.title("ContentAlchemy")
        st.caption("AI-Powered Content Marketing")
        st.divider()

        st.subheader("Content Settings")

        tone = st.selectbox(
            "Brand Tone",
            options=["professional", "conversational", "technical", "inspirational", "educational"],
            index=0,
            help="Sets the writing style for all generated content",
        )

        audience = st.text_input(
            "Target Audience",
            value="marketing professionals",
            help="Who is this content for?",
        )

        st.divider()
        st.subheader("Quick Actions")
        st.caption("Try these prompts:")
        examples = [
            "Research the latest AI trends in 2025",
            "Write a blog about remote work productivity",
            "Create a LinkedIn post about leadership",
            "Generate an image for a tech startup",
            "Build a content strategy for SaaS marketing",
        ]
        for example in examples:
            if st.button(example, use_container_width=True, key=f"ex_{example[:20]}"):
                st.session_state["example_prompt"] = example

        st.divider()
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state["messages"] = []
            st.session_state["last_state"] = {}
            st.rerun()

        st.caption("Powered by Claude Sonnet 4.6 + LangGraph")

    return {"tone": tone, "audience": audience}
