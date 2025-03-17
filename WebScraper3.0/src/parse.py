from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import os
import json
import logging
from dotenv import load_dotenv
import cohere
from groq import Groq
from bs4 import BeautifulSoup
import random
import time
import sys
import os
import subprocess
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Retrieve API keys
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize clients
co = cohere.Client(api_key=COHERE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)
ollama_model = OllamaLLM(model="llama3")

# Define function keywords for task categorization
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]



# Modify the initialization section
# Comment out or replace the existing client initializations
ollama_model = OllamaLLM(model="llama3")



def categorize_query(prompt):
    """
    Categorize user query using Cohere AI.
    Args:
        prompt (str): User query
    Returns:
        list: Categorized tasks
    """
    try:
        response = co.chat(
            model='command-r-plus',
            message=prompt,
            preamble="""You are a Decision-Making Model that categorizes queries.
            Respond with 'general (query)' for general questions,
            'realtime (query)' for queries needing up-to-date information,
            or specific function names for task automation."""
        )
        
        # Process the response
        response_text = response.text.replace("\n", "").split(",")
        response_text = [i.strip() for i in response_text]
        # Filter valid tasks
        valid_tasks = []
        for task in response_text:
            for func in funcs:
                if task.startswith(func):
                    valid_tasks.append(task)
        return valid_tasks if valid_tasks else ["general " + prompt]
    except Exception as e:
        logger.error(f"Error categorizing query: {str(e)}")
        return ["general " + prompt]

def parse_with_ollama(dom_chunks, parse_description, max_retries=3):
    """
    Parse DOM content using Ollama LLM with retry mechanism.
    
    Args:
        dom_chunks (list): List of DOM content chunks
        parse_description (str): Description of what to parse
        max_retries (int): Maximum number of retries
        
    Returns:
        str: Parsed results
    """
    # Define a prompt template
    template = (
        "You are tasked with extracting specific information from the following text content: {dom_content}. "
        "Please follow these instructions carefully: \n\n"
        "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
        "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
        "3. **Empty Response:** If no information matches the description, return an empty string ('')."
        "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    )
    
    # Process with Ollama
    parsed_results = []
    
    for chunk in dom_chunks:
        for attempt in range(max_retries):
            try:
                prompt = template.format(dom_content=chunk, parse_description=parse_description)
                response = ollama_model.invoke(prompt)
                parsed_results.append(response)
                break  # Success, exit retry loop
            except Exception as e:
                logger.error(f"Error parsing chunk (attempt {attempt+1}): {str(e)}")
                if attempt < max_retries - 1:
                    # Add exponential backoff
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Retrying after {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {max_retries} attempts failed for chunk")
                    parsed_results.append(f"Error processing content: {str(e)}")
    
    return "\n".join(parsed_results)


def format_data_with_openai(data, fields=None):
    """
    Format data using OpenAI API.
    Args:
        data (str): Data to format
        fields (list): List of fields to extract
    Returns:
        dict: Formatted data as JSON
    """
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    if fields is None:
        fields = ["Title", "Content", "Author", "Date", "URL"]
    
    system_message = """You are an intelligent text extraction and conversion assistant. Your task is to extract structured information
    from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text,
    with no additional commentary, explanations, or extraneous information.
    Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""
    
    user_message = f"Extract the following information from the provided text: \nPage content: \n\n{data}\n\nInformation to extract: {fields}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        
        if response and response.choices:
            formatted_data = response.choices[0].message.content.strip()
            logger.info(f"Formatted data received from API")
            
            try:
                parsed_json = json.loads(formatted_data)
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error(f"JSON decoding error: {e}")
                raise ValueError("The formatted data could not be decoded into JSON.")
        else:
            raise ValueError("The OpenAI API response did not contain the expected choices data.")
    except Exception as e:
        logger.error(f"Error formatting data with OpenAI: {str(e)}")
        raise
def clean_and_extract_data(html_content, query):
    """
    Clean and extract relevant data from HTML content based on the query.
    
    Args:
        html_content (str): HTML content to process
        query (str): User query to guide extraction
        
    Returns:
        dict: Extracted and cleaned data
    """
    if not html_content:
        return {"error": "No content to process"}
    
    try:
        # Extract body content
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
            element.decompose()
        
        # Extract title
        title = soup.title.string if soup.title else "No title found"
        
        # Extract main content based on common content containers
        main_content = ""
        content_tags = soup.find_all(["article", "main", "div", "section"], class_=lambda c: c and any(x in str(c).lower() for x in ["content", "article", "main", "post"]))
        
        if content_tags:
            for tag in content_tags:
                main_content += tag.get_text(separator="\n", strip=True) + "\n\n"
        else:
            # Fallback to body content
            main_content = soup.body.get_text(separator="\n", strip=True) if soup.body else "No content found"
        
        # Clean up the content
        main_content = "\n".join(line for line in main_content.splitlines() if line.strip())
        
        # Extract metadata
        meta_description = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_description = meta_tag.get("content", "")
        
        # Extract date if available
        date = ""
        date_tags = soup.find_all(["time", "span", "div", "p"], class_=lambda c: c and any(x in str(c).lower() for x in ["date", "time", "published"]))
        if date_tags:
            date = date_tags[0].get_text(strip=True)
        
        return {
            "title": title,
            "meta_description": meta_description,
            "main_content": main_content,
            "date": date,
            "query_relevance": query
        }
    
    except Exception as e:
        logger.error(f"Error cleaning and extracting data: {str(e)}")
        return {"error": str(e)}
