import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Team SEO Link Inserter", layout="wide")

# This pulls the key from the Streamlit Cloud dashboard settings
# so your team doesn't need to see or manage the key.
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing! Please set GEMINI_API_KEY in the Streamlit Secrets.")

st.title("🔗 Link Placement Assistant")
st.info("Input the details below. The AI will rewrite the section to fit the link naturally.")

col1, col2 = st.columns([1, 2])

with col1:
    site_name = st.text_input("Site Name")
    anchor_text = st.text_input("Anchor Text")
    target_url = st.text_input("Target URL")
    
with col2:
    article_content = st.text_area("Article Content", height=300)

if st.button("Generate & Optimize"):
    if not article_content or not anchor_text:
        st.warning("Please fill in the required fields.")
    else:
        with st.spinner("Processing..."):
            prompt = f"""
            You are an expert SEO editor. 
            Insert the link <a href="{target_url}">{anchor_text}</a> naturally into the text below.
            Site context: {site_name}
            
            Original Article:
            {article_content}
            
            Return the full article with the link inserted.
            """
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            st.subheader("Result")
            st.code(response.text, language="html") # Using code block makes it easy for the team to copy
