from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from googlesearch import search
import os
import time
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def google_search(query, num_results=10):
    """
    Perform a Google search and return a list of URLs.
    Args:
        query (str): The search query
        num_results (int): Number of results to return
    Returns:
        list: List of URLs from search results
    """
    try:
        results = []
        for url in search(query, num_results=num_results):
            results.append(url)
            time.sleep(1)  # Add delay between collecting results
        return results
    except Exception as e:
        logger.error(f"Error during Google search: {str(e)}")
        return []

#def scrape_website(url):
    """
    Scrape a website and return its HTML content.
    Args:
        url (str): The URL to scrape
    Returns:
        str: HTML content of the website
    """
    logger.info(f"Scraping website: {url}")
    try:
        # Set up Chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=options)
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        # Navigate to the URL
        driver.get(url)
        
        # Wait for the body element to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Wait for dynamic content to load
        time.sleep(5)
        
        # Get the page source
        html = driver.page_source
        
        # Close the driver
        driver.quit()
        
        return html
    except Exception as e:
        logger.error(f"An error occurred while scraping: {str(e)}")
        return None

def scrape_website(url, use_proxy=False):
    """
    Scrape a website and return its HTML content.
    Args:
        url (str): The URL to scrape
        use_proxy (bool): Whether to use a proxy
    Returns:
        str: HTML content of the website
    """
    logger.info(f"Scraping website: {url}")
    try:
        # Set up Chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        
        # Add proxy if requested
        if use_proxy and os.getenv("PROXY_SERVER"):
            proxy_server = os.getenv("PROXY_SERVER")
            options.add_argument(f'--proxy-server={proxy_server}')

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=options)
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        # Navigate to the URL
        driver.get(url)
        
        # Wait for the body element to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Wait for dynamic content to load
        time.sleep(5)
        
        # Get the page source
        html = driver.page_source
        
        # Close the driver
        driver.quit()
        
        return html
    except Exception as e:
        logger.error(f"An error occurred while scraping: {str(e)}")
        return None


def extract_body_content(html_content):
    """
    Extract the body content from HTML.
    Args:
        html_content (str): HTML content
    Returns:
        str: Body content as a string
    """
    if html_content is None:
        return ""
    
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    """
    Clean the body content by removing scripts, styles, etc.
    Args:
        body_content (str): Body content to clean
    Returns:
        str: Cleaned content
    """
    if not body_content:
        return ""
    
    soup = BeautifulSoup(body_content, "html.parser")
    
    # Remove unwanted elements
    for element in soup(["script", "style", "nav", "header", "footer", "iframe", "noscript"]):
        element.decompose()
    
    # Get text with line breaks
    cleaned_content = soup.get_text(separator="\n")
    
    # Remove empty lines
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """
    Split the DOM content into chunks of specified maximum length.
    Args:
        dom_content (str): DOM content to split
        max_length (int): Maximum length of each chunk
    Returns:
        list: List of content chunks
    """
    return [dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)]
