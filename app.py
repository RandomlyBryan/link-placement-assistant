import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="Link placement assistant",
    page_icon="🔗",
    layout="wide"
)

# 2. API Key Setup
# We use st.secrets so the key stays hidden from the public
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Go to Streamlit Settings > Secrets and add: GEMINI_API_KEY = 'your_key'")

# 3. UI Header
st.title("🔗 SEO Link Placement Assistant")
st.markdown("Designed for the team to insert links naturally.")

# 4. Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Link Details")
    site_name = st.text_input("Target Site Name", placeholder="e.g. https://example.com")
    target_url = st.text_input("Target URL", placeholder="https://example.com/page")
    anchor_text = st.text_input("Anchor Text", placeholder="e.g. Anchor text here")
    
with col2:
    st.subheader("Article Content")
    article_content = st.text_area("Paste your article here:", height=300)

# 5. Execution Logic
if st.button("Generate Optimized Article", type="primary"):
    if not article_content or not anchor_text or not target_url:
        st.warning("Please fill in the Article, Anchor Text, and URL.")
    else:
        with st.spinner("AI is analyzing and inserting the link..."):
            try:
                prompt = f"""
                You are a senior SEO Editor. Your task is to insert a backlink naturally into the provided article.
                
                Link Info:
                - Site Name: {site_name}
                - Target URL: {target_url}
                - Anchor Text: {anchor_text}
                
                Article Content:
                {article_content}
                
                Guidelines:
                1. Insert the link <a href="{target_url}">{anchor_text}</a> into the most relevant paragraph.
                2. Ensure the sentence flow remains natural and professional.
                3. Return the FULL updated article including the HTML link.
                """
                
                # Updated to the current 2026 stable model
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(prompt)
                final_text = response.text
                
                # Display Result
                st.divider()
                st.subheader("Final Optimized Article")
                
                # st.code provides a 'copy' button automatically
                st.code(final_text, language="html")
                
                # Download Button for the team
                st.download_button(
                    label="Download Article as .txt",
                    data=final_text,
                    file_name=f"optimized_{site_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
