import streamlit as st
import os
import time
import json
import logging
import random
from datetime import datetime
from dotenv import load_dotenv

# Import local modules
from scrape import google_search, scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama, format_data_with_openai, clean_and_extract_data
from model import categorize_query, process_with_groq, process_with_ollama, save_chat_log
from utils import setup_logging, save_data, save_json, save_csv

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Streamlit UI
st.set_page_config(page_title="Web Scraper 3.0", layout="wide")
st.title("Web Scraper 3.0")

# Initialize session state
if 'scraped_urls' not in st.session_state:
    st.session_state.scraped_urls = []
if 'current_data' not in st.session_state:
    st.session_state.current_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Function to perform Google search with retry
def google_search_with_retry(query, num_results=10):
    max_retries = 5
    retry_delay = 2  # Initial delay in seconds
    for attempt in range(max_retries):
        try:
            results = google_search(query, num_results=num_results)
            if results:
                return results
        except Exception as e:
            logger.error(f"Error during Google search attempt {attempt+1}: {str(e)}")
            if attempt < max_retries - 1:
                retry_delay *= 2  # Exponential backoff
                time.sleep(retry_delay + random.uniform(0, 1))  # Add some randomness to the delay
            else:
                logger.error(f"Failed to retrieve Google search results after {max_retries} attempts.")
                return []
    return []

# Sidebar for mode selection
st.sidebar.title("Mode Selection")
mode = st.sidebar.radio("Choose Mode", ["URL Scraping", "Search Query", "Chat with Data"])

if mode == "URL Scraping":
    st.header("URL Scraping Mode")
    
    # URL input
    url = st.text_input("Enter Website URL")
    
    # Anti-scraping options
    with st.expander("Advanced Options"):
        use_proxy = st.checkbox("Use Proxy", value=False)
        rotate_user_agent = st.checkbox("Rotate User Agent", value=True)
        delay_time = st.slider("Delay Time (seconds)", 1, 10, 5)
    
    if st.button("Scrape Website"):
        if url:
            try:
                with st.spinner("Scraping the website..."):
                    # Scrape the website with anti-scraping measures
                    html_content = scrape_website(url, use_proxy=use_proxy)
                    
                    if html_content:
                        body_content = extract_body_content(html_content)
                        cleaned_content = clean_body_content(body_content)
                        
                        # Store the DOM content in session state
                        st.session_state.current_data = cleaned_content
                        
                        # Add to scraped URLs
                        if url not in st.session_state.scraped_urls:
                            st.session_state.scraped_urls.append(url)
                        
                        # Save raw data
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        save_data(cleaned_content, f"raw_data_{timestamp}.txt", folder="data/raw_data")
                        
                        # Display the DOM content in an expandable section
                        with st.expander("View Scraped Content"):
                            st.text_area("Content", cleaned_content, height=300)
                        
                        st.success(f"Website scraped successfully! Content saved to data/raw_data/raw_data_{timestamp}.txt")
                    else:
                        st.error("Failed to scrape the website. Please check the URL and try again.")
            except Exception as e:
                logger.error(f"Error scraping website: {str(e)}")
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a URL before scraping.")
    
    # Parse content section
    st.subheader("Parse Content")
    
    if st.session_state.current_data:
        parse_description = st.text_area("Describe what you want to extract from the content")
        
        # In the URL Scraping section, modify the parse content button handler
if st.button("Parse Content"):
    if parse_description:
        try:
            with st.spinner("Parsing content..."):
                # Split content into chunks for processing
                dom_chunks = split_dom_content(st.session_state.current_data)
                
                # Parse with local LLM
                parsed_result = parse_with_ollama(dom_chunks, parse_description, max_retries=3)
                
                # Save parsed result
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_data(parsed_result, f"parsed_data_{timestamp}.txt", folder="data/processed_data")
                
                # Display result
                st.text_area("Parsed Result", parsed_result, height=300)
                
                # Format with local LLM if needed
                if st.checkbox("Format with Local LLM"):
                    with st.spinner("Formatting with Local LLM..."):
                        formatted_data = format_data_with_openai(parsed_result)
                        
                        # Save formatted data
                        save_data(json.dumps(formatted_data, indent=4),
                                f"formatted_data_{timestamp}.json",
                                folder="data/processed_data")
                        
                        # Display formatted data
                        st.json(formatted_data)
        except Exception as e:
            logger.error(f"Error parsing content: {str(e)}")
            st.error(f"An error occurred during parsing: {str(e)}")

        #if st.button("Parse Content"):
            if parse_description:
                try:
                    with st.spinner("Parsing content..."):
                        # Split content into chunks for processing
                        dom_chunks = split_dom_content(st.session_state.current_data)
                        
                        # Parse with Ollama
                        parsed_result = parse_with_ollama(dom_chunks, parse_description, max_retries=3)
                        
                        # Save parsed result
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        save_data(parsed_result, f"parsed_data_{timestamp}.txt", folder="data/processed_data")
                        
                        # Display result
                        st.text_area("Parsed Result", parsed_result, height=300)
                        
                        # Format with OpenAI if needed
                        if st.checkbox("Format with OpenAI"):
                            with st.spinner("Formatting with OpenAI..."):
                                formatted_data = format_data_with_openai(parsed_result)
                                
                                # Save formatted data
                                save_json(formatted_data,
                                        f"formatted_data_{timestamp}.json",
                                        folder="data/processed_data")
                                
                                # Display formatted data
                                st.json(formatted_data)
                                
                                # Option to save as CSV
                                if st.button("Save as CSV"):
                                    save_csv([formatted_data], 
                                            f"formatted_data_{timestamp}.csv",
                                            folder="data/processed_data")
                                    st.success(f"Data saved as CSV: data/processed_data/formatted_data_{timestamp}.csv")
                except Exception as e:
                    logger.error(f"Error parsing content: {str(e)}")
                    st.error(f"An error occurred during parsing: {str(e)}")
            else:
                st.warning("Please describe what you want to extract.")
    else:
        st.info("Please scrape a website first to parse its content.")

elif mode == "Search Query":
    st.header("Search Query Mode")
    
    # Search query input
    query = st.text_input("Enter your search query")
    num_results = st.slider("Number of results to fetch", 5, 20, 10)
    
    if st.button("Search"):
        if query:
            try:
                with st.spinner(f"Searching for '{query}'..."):
                    # Perform Google search with retry
                    search_results = google_search_with_retry(query, num_results=num_results)
                    
                    if search_results:
                        # Store results in session state for further processing
                        st.session_state.search_results = search_results
                        
                        # Display search results
                        st.subheader("Search Results")
                        for i, url in enumerate(search_results, 1):
                            st.write(f"{i}. {url}")
                        
                        # Save search results
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        save_data("\n".join(search_results),
                                f"search_results_{timestamp}.txt",
                                folder="data/raw_data")
                        
                        # Add auto-scrape option
                        auto_scrape = st.checkbox("Auto-scrape top results", value=True)
                        num_to_scrape = st.slider("Number of results to auto-scrape", 1, len(search_results), min(3, len(search_results)))
                        
                        if auto_scrape:
                            scraped_contents = []
                            progress_bar = st.progress(0)
                            
                            for i, url in enumerate(search_results[:num_to_scrape]):
                                try:
                                    with st.spinner(f"Scraping {i+1}/{num_to_scrape}: {url}"):
                                        html_content = scrape_website(url)
                                        if html_content:
                                            body_content = extract_body_content(html_content)
                                            cleaned_content = clean_body_content(body_content)
                                            
                                            # Use enhanced data extraction
                                            extracted_data = clean_and_extract_data(html_content, query)
                                            
                                            scraped_contents.append({
                                                "url": url,
                                                "content": cleaned_content,
                                                "extracted_data": extracted_data
                                            })
                                            
                                            # Add to scraped URLs
                                            if url not in st.session_state.scraped_urls:
                                                st.session_state.scraped_urls.append(url)
                                except Exception as e:
                                    logger.error(f"Error scraping {url}: {str(e)}")
                                    st.warning(f"Failed to scrape {url}: {str(e)}")
                                
                                # Update progress
                                progress_bar.progress((i + 1) / num_to_scrape)
                            
                            # Save all scraped contents
                            if scraped_contents:
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                save_json(scraped_contents,
                                        f"bulk_scrape_{timestamp}.json",
                                        folder="data/raw_data")
                                st.success(f"Scraped {len(scraped_contents)} websites successfully!")
                                
                                # Process with AI automatically
                                st.subheader("AI Analysis")
                                combined_content = "\n\n".join([item["content"] for item in scraped_contents])
                                system_message = f"You are analyzing content related to the search query: {query}. Provide a comprehensive summary."
                                
                                with st.spinner("Processing with AI..."):
                                    ai_response = process_with_groq(combined_content, system_message)
                                    
                                    # Save AI response
                                    save_data(ai_response,
                                            f"ai_response_{timestamp}.txt",
                                            folder="data/processed_data")
                                    
                                    # Display AI response
                                    st.write(ai_response)
                                    
                                    # Option to save as structured data
                                    if st.button("Extract Structured Data"):
                                        with st.spinner("Extracting structured data..."):
                                            structured_data = format_data_with_openai(ai_response)
                                            save_json(structured_data,
                                                    f"structured_data_{timestamp}.json",
                                                    folder="data/processed_data")
                                            st.json(structured_data)
                    else:
                        st.warning("No search results found. Try a different query.")
            except Exception as e:
                logger.error(f"An error occurred during search: {str(e)}")
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a search query.")

elif mode == "Chat with Data":
    st.header("Chat with Data Mode")
    
    # Display scraped URLs
    if st.session_state.scraped_urls:
        st.subheader("Scraped Websites")
        for url in st.session_state.scraped_urls:
            st.write(f"- {url}")
    else:
        st.info("No websites have been scraped yet. Use the URL Scraping or Search Query mode to scrape websites.")
    
    # Chat interface
    st.subheader("Chat")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**AI:** {message['content']}")
    
    # User input
    user_input = st.text_input("Ask a question about the scraped data")
    
    if st.button("Send"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Process user query
            query_type = categorize_query(user_input)
            
            if "realtime" in query_type[0]:
                # Handle realtime query
                with st.spinner("Searching for up-to-date information..."):
                    search_results = google_search_with_retry(user_input, num_results=5)
                    
                    if search_results:
                        # Scrape first result
                        html_content = scrape_website(search_results[0])
                        
                        if html_content:
                            body_content = extract_body_content(html_content)
                            cleaned_content = clean_body_content(body_content)
                            
                            # Process with AI
                            system_message = f"You are answering a question based on the latest information from the web. The question is: {user_input}"
                            ai_response = process_with_groq(cleaned_content, system_message)
                        else:
                            ai_response = "I couldn't retrieve the latest information. Please try a different question."
                    else:
                        ai_response = "I couldn't find relevant information for your query."
            else:
                # Handle general query using existing data
                if st.session_state.scraped_urls:
                    # Combine all scraped data
                    combined_data = ""
                    for url in st.session_state.scraped_urls[:5]:  # Limit to 5 most recent
                        try:
                            html_content = scrape_website(url)
                            if html_content:
                                body_content = extract_body_content(html_content)
                                cleaned_content = clean_body_content(body_content)
                                combined_data += f"\nContent from {url}:\n{cleaned_content}\n\n"
                        except Exception as e:
                            logger.error(f"Error retrieving data from {url}: {str(e)}")
                    
                    if combined_data:
                        system_message = f"You are answering a question based on the provided data. The question is: {user_input}"
                        ai_response = process_with_groq(combined_data, system_message)
                    else:
                        ai_response = "I couldn't retrieve the data from the scraped websites."
                else:
                    ai_response = "I don't have any data to reference. Please scrape some websites first."
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Save chat history
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_json(st.session_state.chat_history,
                    f"chat_history_{timestamp}.json",
                    folder="data/processed_data")
            
            # Save to chat log
            save_chat_log(st.session_state.chat_history)
            
            # Rerun to display the updated chat
            st.rerun()

# Add a footer
st.sidebar.markdown("---")
st.sidebar.info("Web Scraper 3.0 - Developed on March 9, 2025")
