import streamlit as st


ROUTE_ICONS = {
    "research": "🔍",
    "blog": "✍️",
    "linkedin": "💼",
    "image": "🎨",
    "strategy": "📋",
}

ROUTE_LABELS = {
    "research": "Research Report",
    "blog": "SEO Blog Post",
    "linkedin": "LinkedIn Post",
    "image": "Generated Image",
    "strategy": "Content Strategy",
}


def render_chat_history(messages: list[dict]) -> None:
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def render_user_message(content: str) -> None:
    with st.chat_message("user"):
        st.markdown(content)


def render_assistant_response(state: dict) -> None:
    route = state.get("route", "research")
    icon = ROUTE_ICONS.get(route, "🤖")
    label = ROUTE_LABELS.get(route, "Response")
    content_output = state.get("content_output", "")
    image_url = state.get("image_url")
    error = state.get("error")

    with st.chat_message("assistant"):
        if error and not content_output:
            st.error(f"Error: {error}")
            return

        st.markdown(f"**{icon} {label}**")
        st.divider()

        if image_url:
            st.image(image_url, caption=f"Generated: {state.get('topic', '')}", use_container_width=True)

        if content_output:
            st.markdown(content_output)

        _render_metadata(state)


def _render_metadata(state: dict) -> None:
    seo = state.get("seo_metadata", {})
    quality = state.get("quality_score", {})

    if not seo and not quality:
        return

    with st.expander("Content Analytics", expanded=False):
        col1, col2 = st.columns(2)

        if quality:
            with col1:
                score = quality.get("score", 0)
                color = "green" if score >= 80 else "orange" if score >= 60 else "red"
                st.metric("Quality Score", f"{score}/100")
                wc = quality.get("word_count", 0)
                st.metric("Word Count", wc)
                issues = quality.get("issues", [])
                if issues:
                    st.warning("\n".join(f"• {i}" for i in issues))
                suggestions = quality.get("suggestions", [])
                if suggestions:
                    with st.expander("Suggestions"):
                        for s in suggestions:
                            st.info(f"💡 {s}")

        if seo:
            with col2:
                seo_score = seo.get("seo_score", {})
                if isinstance(seo_score, dict):
                    st.metric("SEO Score", f"{seo_score.get('score', 0)}/100")
                keywords = seo.get("keywords", [])
                if keywords:
                    st.markdown("**Top Keywords:**")
                    st.write(", ".join(keywords[:7]))
                meta = seo.get("meta_description", "")
                if meta:
                    st.markdown("**Meta Description:**")
                    st.caption(meta)
