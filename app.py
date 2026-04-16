import streamlit as st
import google.generativeai as genai
import re

# 1. Page Configuration
st.set_page_config(
    page_title="Link Placement Assistant",
    page_icon="🔗",
    layout="wide"
)

# 2. CUSTOM CSS: Forces text wrapping in code blocks
st.markdown("""
    <style>
    code {
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
    .preview-box {
        border: 1px solid #444; 
        padding: 15px; 
        border-radius: 8px; 
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API Key Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")

# 4. Refresh Logic (Session State)
def clear_text():
    st.session_state["site_name"] = ""
    st.session_state["target_url"] = ""
    st.session_state["anchor_text"] = ""
    st.session_state["article_content"] = ""

# 5. Sidebar & Clear Button
with st.sidebar:
    st.title("RandomlyAI")
    st.button("Clear All Fields", on_click=clear_text, help="Click to reset the app.")
    st.divider()
    st.info("Optimize link placements without disrupting flow.")

# 6. UI Header
st.title("🔗 Link Placement Assistant")

# 7. Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Link Details")
    site_name = st.text_input("Target Site Name", key="site_name")
    target_url = st.text_input("Target URL", key="target_url")
    anchor_text = st.text_input("Anchor Text", key="anchor_text")
    
with col2:
    st.subheader("Article Content")
    article_content = st.text_area("Paste your article here:", height=300, key="article_content")

# 8. Execution Logic
if st.button("Generate Placement Options", type="primary"):
    if not article_content or not anchor_text or not target_url:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Analyzing semantic flow..."):
            try:
                # Keep the requested model name but use System Instructions for better reliability
                model = genai.GenerativeModel(
                    model_name='gemini-3-flash-preview',
                    system_instruction="You are a senior SEO Editor. Follow the OPTION_START, ORIGINAL, REVISED, OPTION_END format exactly."
                )

                prompt = f"""
                Provide 3 different options for inserting a backlink.
                
                Link Info:
                - URL: {target_url}
                - Anchor Text: {anchor_text}
                - Target Context: {site_name}
                
                Article Content:
                {article_content}
                
                STRICT EDITORIAL RULES:
                1. ANALYZE: Scan for themes related to "{anchor_text}".
                2. PLACEMENT: Rewrite the surrounding sentence to bridge the original thought with the new link.
                3. FLOW: Natural, professional tone. No "Click here" styles.
                
                OUTPUT FORMAT:
                OPTION_START
                ORIGINAL: [Paragraph text]
                REVISED: [Rewritten paragraph with <a href="{target_url}">{anchor_text}</a>]
                OPTION_END
                """
                
                response = model.generate_content(prompt)
                raw_text = response.text

                # Robust regex: handles extra spaces or newlines gracefully
                pattern = r"OPTION_START\s*ORIGINAL:\s*(.*?)\s*REVISED:\s*(.*?)\s*OPTION_END"
                options = re.findall(pattern, raw_text, re.DOTALL)

                st.divider()

                if not options:
                    st.error("Formatting error. The AI didn't follow the tag structure.")
                    with st.expander("View Raw Output"):
                        st.text(raw_text)
                else:
                    for i, (original, revised) in enumerate(options, 1):
                        st.subheader(f"Option {i}")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.caption("Original Paragraph")
                            st.code(original.strip(), language=None)
                        with c2:
                            st.caption("Live Preview")
                            st.markdown(f'<div class="preview-box">{revised.strip()}</div>', unsafe_allow_html=True)
                            st.caption("HTML Output")
                            st.code(revised.strip(), language="html")
                        st.divider()

            except Exception as e:
                st.error(f"Error: {e}")
