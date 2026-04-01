import streamlit as st
import google.generativeai as genai
import re

# 1. Page Configuration
st.set_page_config(
    page_title="Link Placement Assistant",
    page_icon="🔗",
    layout="wide"
)

# 2. API Key Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")

# 3. UI Header
st.title("🔗 Precision SEO Link Placement Assistant")
st.markdown("Advanced AI agent trained to prioritize natural content flow and link relevance.")

# 4. Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Link Details")
    site_name = st.text_input("Target Site Name")
    target_url = st.text_input("Target URL")
    anchor_text = st.text_input("Anchor Text")
    
with col2:
    st.subheader("Article Content")
    article_content = st.text_area("Paste your article here:", height=300)

# 5. Execution Logic
if st.button("Generate 3 Natural Options", type="primary"):
    if not article_content or not anchor_text or not target_url:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Agent is analyzing semantic flow..."):
            try:
                # ENHANCED PROMPT FOR NATURAL FLOW
                prompt = f"""
                You are a Senior Content Strategist and SEO Editor. Your goal is to insert a backlink so naturally that a reader wouldn't realize it was added later.
                
                Link Metadata:
                - URL: {target_url}
                - Anchor Text: {anchor_text}
                - Target Context: {site_name}
                
                Article Content:
                {article_content}
                
                STRICT EDITORIAL RULES:
                1. ANALYZE: Scan the article for themes directly related to "{anchor_text}" or "{site_name}".
                2. PLACEMENT: Do not just drop the link. Rewrite the surrounding sentence to bridge the original thought with the new link seamlessly.
                3. FLOW: Ensure the transition into the anchor text is grammatically perfect. Avoid "Click here" or "Check out this link" styles.
                4. VARIETY: Provide 3 distinct placement options in different parts of the article (Introduction, Body, Conclusion).
                
                OUTPUT FORMAT (STRICT):
                OPTION_START
                ORIGINAL: [Paragraph text before any changes]
                REVISED: [The fully rewritten paragraph with <a href="{target_url}">{anchor_text}</a> integrated naturally]
                OPTION_END
                """
                
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(prompt)
                raw_text = response.text

                options = re.findall(r"OPTION_START\nORIGINAL: (.*?)\nREVISED: (.*?)\nOPTION_END", raw_text, re.DOTALL)

                st.divider()

                if not options:
                    st.error("The AI had trouble formatting the response. Please try clicking the button again.")
                    st.write("Raw Output for debugging:", raw_text)
                else:
                    for i, (original, revised) in enumerate(options, 1):
                        st.subheader(f"Option {i}")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.caption("Original Paragraph (Wrapped)")
                            st.text_area(f"Orig_{i}", value=original.strip(), height=160, disabled=True, label_visibility="collapsed")
                        
                        with c2:
                            st.caption("Revised Paragraph (Live Preview)")
                            # Live rendered version for the team to see the link
                            st.markdown(f'<div style="border:1px solid #444; padding:15px; border-radius:8px; background-color:#1e1e1e;">{revised.strip()}</div>', unsafe_allow_html=True)
                            
                            # Code block with Copy button
                            st.code(revised.strip(), language="html")
                        
                        st.divider()

            except Exception as e:
                st.error(f"Error: {e}")
