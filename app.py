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
st.title("🔗 SEO Link Inserter (Copy-Ready Mode)")
st.markdown("Select a placement option below and use the copy icon in the top-right of each box.")

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
if st.button("Generate 3 Placement Options", type="primary"):
    if not article_content or not anchor_text or not target_url:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Generating options..."):
            try:
                prompt = f"""
                You are a senior SEO Editor. Provide 3 different options for inserting a backlink.
                
                Link Info:
                - Target URL: {target_url}
                - Anchor Text: {anchor_text}
                
                Article:
                {article_content}
                
                For each of the 3 options, provide:
                1. The Original Paragraph.
                2. The Revised Paragraph with the HTML link <a href="{target_url}">{anchor_text}</a>.
                
                Format your response exactly like this so I can parse it:
                OPTION_START
                ORIGINAL: [Paragraph]
                REVISED: [Paragraph with link]
                OPTION_END
                """
                
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(prompt)
                raw_text = response.text

                # Parsing the 3 options
                options = re.findall(r"OPTION_START\nORIGINAL: (.*?)\nREVISED: (.*?)\nOPTION_END", raw_text, re.DOTALL)

                st.divider()

                for i, (original, revised) in enumerate(options, 1):
                    st.subheader(f"Option {i}")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.caption("Original Section (For Reference)")
                        st.code(original.strip(), language=None) # Clickable copy button here
                    
                    with c2:
                        st.caption("Revised Section (Copy for CMS)")
                        st.code(revised.strip(), language="html") # Clickable copy button here
                        
                        # Visual Preview (Clickable link for testing)
                        st.markdown("**Live Preview:**")
                        st.markdown(revised.strip(), unsafe_allow_html=True)
                    
                    st.divider()

            except Exception as e:
                st.error(f"An error occurred: {e}. If this persists, try clicking generate again.")
