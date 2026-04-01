import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="Scalerrs SEO Link Inserter",
    page_icon="🔗",
    layout="wide"
)

# 2. API Key Configuration (Using Streamlit Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Cloud Secrets.")
    st.stop()

# 3. UI Header
st.title("🔗 Link Placement Assistant")
st.markdown("""
Use this tool to naturally insert backlinks into your articles. 
The AI will maintain the original tone while ensuring the anchor text flows perfectly.
""")

# 4. Input Section
with st.container():
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("Link Details")
        site_name = st.text_input("Target Domain", placeholder="e.g., "https://sample.com/")
        anchor_text = st.text_input("Anchor Text", placeholder="e.g., anchor text here")
        target_url = st.text_input("Target URL", placeholder="https://sample.com/content-slug-here")
        
        st.divider()
        generate_btn = st.button("🚀 Generate Optimized Article", use_container_width=True)

    with col2:
        st.subheader("Article Content")
        article_content = st.text_area(
            "Paste the original article here:", 
            height=400,
            placeholder="Once upon a time in the world of SEO..."
        )

# 5. Processing Logic
if generate_btn:
    if not article_content or not anchor_text or not target_url:
        st.warning("Please fill in the Anchor Text, URL, and Article Content.")
    else:
        with st.spinner("Analyzing text and inserting link..."):
            try:
                # Using Gemini 3 Flash for the best balance of speed and SEO logic
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are a Senior SEO Content Editor. Your goal is to insert a backlink into an article so naturally that a reader wouldn't realize it was added later.
                
                CONTEXT:
                - Target Site: {site_name}
                - Anchor Text: {anchor_text}
                - Target URL: {target_url}
                
                ORIGINAL ARTICLE:
                {article_content}
                
                INSTRUCTIONS:
                1. Insert the link <a href="{target_url}">{anchor_text}</a> into the most relevant paragraph.
                2. If the exact anchor text doesn't exist, slightly rewrite a sentence to include it naturally.
                3. Do not change the overall meaning or tone of the article.
                4. Fix any obvious SEO or grammatical errors you find.
                5. RETURN THE FULL UPDATED ARTICLE IN HTML FORMAT.
                """
                
                response = model.generate_content(prompt)
                
                # 6. Results Display
                st.success("Link successfully inserted!")
                
                tabs = st.tabs(["Preview", "HTML Code"])
                
                with tabs[0]:
                    st.markdown(response.text, unsafe_content=True)
                
                with tabs[1]:
                    st.code(response.text, language="html")
                
                # Download Button
                st.download_button(
                    label="Download as Text File",
                    data=response.text,
                    file_name=f"optimized_{site_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Tip: Double-check your API key and internet connection.")
