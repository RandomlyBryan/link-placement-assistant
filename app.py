import streamlit as st
import google.generativeai as genai

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
st.title("🔗 SEO Link Inserter (Options Mode)")
st.markdown("Generate 3 different placement options for your backlink.")

# 4. Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Link Details")
    site_name = st.text_input("Domain Name", placeholder="e.g. https://example.com/")
    target_url = st.text_input("Target URL", placeholder="https://example.com/page")
    anchor_text = st.text_input("Anchor Text", placeholder="e.g. digital marketing agency")
    
with col2:
    st.subheader("Article Content")
    article_content = st.text_area("Paste your article here:", height=300)

# 5. Execution Logic
if st.button("Generate 3 Placement Options", type="primary"):
    if not article_content or not anchor_text or not target_url:
        st.warning("Please fill in the Article, Anchor Text, and URL.")
    else:
        with st.spinner("Finding the 3 best spots..."):
            try:
                prompt = f"""
                You are a senior SEO Editor. Your task is to provide 3 different options for inserting a backlink.
                
                Link Info:
                - Target URL: {target_url}
                - Anchor Text: {anchor_text}
                
                Article:
                {article_content}
                
                Task:
                Find 3 different paragraphs where the anchor text could fit naturally.
                
                Format the response EXACTLY like this for each option:
                
                ### Option [Number]
                **Original Section:**
                [The original paragraph]
                
                **Revised Section:**
                [The rewritten paragraph with <a href="{target_url}">{anchor_text}</a> inserted naturally]
                
                ---
                """
                
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(prompt)
                
                st.divider()
                # Display the 3 options
                st.markdown(response.text)
                
                # Copy friendly block for the team
                with st.expander("Show Raw HTML for Copying"):
                    st.code(response.text, language="html")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
