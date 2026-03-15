import streamlit as st


def render_content_preview(state: dict) -> None:
    route = state.get("route", "")
    content_output = state.get("content_output", "")
    image_url = state.get("image_url")

    if not content_output and not image_url:
        return

    st.subheader("Content Preview & Export")

    tabs = ["Content", "Copy-Ready", "Metadata"]
    tab1, tab2, tab3 = st.tabs(tabs)

    with tab1:
        if image_url:
            st.image(image_url, use_container_width=True)
        if content_output:
            st.markdown(content_output)

    with tab2:
        st.caption("Click to copy the raw content")
        if content_output:
            st.code(content_output, language="markdown")
        if image_url:
            st.text_input("Image URL", value=image_url)

    with tab3:
        seo = state.get("seo_metadata", {})
        quality = state.get("quality_score", {})

        if quality:
            st.markdown("**Quality Metrics**")
            cols = st.columns(3)
            cols[0].metric("Quality Score", f"{quality.get('score', 0)}/100")
            cols[1].metric("Word Count", quality.get("word_count", 0))
            cols[2].metric("Status", "✅ Pass" if quality.get("passed") else "⚠️ Review")

            issues = quality.get("issues", [])
            if issues:
                st.warning("Issues Found:\n" + "\n".join(f"• {i}" for i in issues))

        if seo:
            st.markdown("**SEO Metadata**")
            seo_score = seo.get("seo_score", {})
            if isinstance(seo_score, dict):
                st.metric("SEO Score", f"{seo_score.get('score', 0)}/100")
                details = seo_score.get("details", {})
                for k, v in details.items():
                    st.caption(f"**{k.replace('_', ' ').title()}:** {v}")

            keywords = seo.get("keywords", [])
            if keywords:
                st.markdown(f"**Keywords:** {', '.join(keywords)}")

            meta = seo.get("meta_description", "")
            if meta:
                st.text_area("Meta Description (copy this)", value=meta, height=80)
