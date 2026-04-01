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
st.title("🔗 SEO Link Placement Assistant")
st.markdown("Enter details to naturally insert a backlink into your content.")

# 4. Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Link Details")
    site_name = st.text_input("Target Site Name", placeholder="e.g. https://example.com/")
    target_url = st.text_input("Target URL", placeholder="https://example.com/page")
    anchor_text = st.text_input("Anchor Text", placeholder="e.g. Abchor Text Here")
    
with col2:
    st.subheader("Article Content")
    article_content = st.text_area("Paste your article here:", height=300)

# 5. Execution Logic
if st.button("Generate Optimized Article", type="primary"):
    if not article_content or not anchor_text or not target_url:
        st.warning("Please fill in the Article, Anchor Text, and URL.")
    else:
        with st.spinner("Finding the best placement..."):
            try:
                # Updated prompt to match the specific format from our chat
                prompt = f"""
                You are a senior SEO Editor.
                
                Context:
                - Target Site: {site_name}
                - Target URL: {target_url}
                - Anchor Text: {anchor_text}
                
                Article:
                {article_content}
                
                Task:
                1. Identify the most relevant paragraph to insert the anchor text.
                2. Rewrite that paragraph to naturally include: <a href="{target_url}">{anchor_text}</a>.
                3. Ensure the flow is seamless and professional.
                
                Response Format:
                ### Revised Section:
                [Show ONLY the paragraph where the link was inserted here]
                
                ### Full Optimized Article:
                [Provide the full article here with the link included]
                """
                
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(prompt)
                final_output = response.text
                
                st.divider()
                # Display the result using markdown so the headings and code blocks look right
                st.markdown(final_output)
                
                # Add a copy-friendly raw version for the team
                with st.expander("Show Raw HTML for Copying"):
                    st.code(final_output, language="html")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
