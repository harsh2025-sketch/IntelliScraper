import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Import local modules
try:
    from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
    from parse import parse_with_ollama
    from utils import setup_logging, save_data
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Setup
setup_logging()
load_dotenv()

# Page config
st.set_page_config(
    page_title="IntelliScraper",
    page_icon="🧠",
    layout="centered"
)

# Header
st.title("🧠 IntelliScraper")
st.markdown("**AI-Powered Web Scraping Made Simple**")
st.divider()

# Main interface
url = st.text_input("🌐 Enter Website URL", placeholder="https://example.com")

if st.button("🚀 Scrape Website", type="primary", use_container_width=True):
    if url:
        with st.spinner("⏳ Scraping website..."):
            try:
                # Scrape website
                html_content = scrape_website(url)
                
                if html_content:
                    body_content = extract_body_content(html_content)
                    cleaned_content = clean_body_content(body_content)
                    
                    # Save data
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_data(cleaned_content, f"scraped_{timestamp}.txt", folder="data/raw_data")
                    
                    # Display success
                    st.success("✅ Website scraped successfully!")
                    
                    # Show content
                    with st.expander("📄 View Scraped Content"):
                        st.text_area("Content", cleaned_content, height=300, label_visibility="collapsed")
                    
                    # Parse section
                    st.divider()
                    st.subheader("🤖 Extract Specific Information")
                    
                    parse_query = st.text_input(
                        "What would you like to extract?",
                        placeholder="e.g., product prices, contact information, article headlines"
                    )
                    
                    if st.button("✨ Extract", use_container_width=True):
                        if parse_query:
                            with st.spinner("🔍 Analyzing content..."):
                                try:
                                    dom_chunks = split_dom_content(cleaned_content)
                                    parsed_result = parse_with_ollama(dom_chunks, parse_query)
                                    
                                    # Save parsed data
                                    save_data(parsed_result, f"parsed_{timestamp}.txt", folder="data/processed_data")
                                    
                                    # Display result
                                    st.success("✅ Extraction complete!")
                                    st.markdown("### 📊 Results")
                                    st.write(parsed_result)
                                    
                                except Exception as e:
                                    st.error(f"❌ Extraction failed: {str(e)}")
                        else:
                            st.warning("⚠️ Please describe what you want to extract")
                else:
                    st.error("❌ Failed to scrape website. Please check the URL.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a URL")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>💾 Scraped data is saved in <code>data/</code> folder</p>
        <p>Made with ❤️ by <a href='https://github.com/harsh2025-sketch' target='_blank'>Harsh</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
