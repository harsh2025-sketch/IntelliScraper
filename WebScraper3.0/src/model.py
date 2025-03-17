import cohere
from langchain_ollama import OllamaLLM
from groq import Groq
from dotenv import load_dotenv
import os
import logging
import json
# Add these imports
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



# Add a function to call your local LLM
def call_local_llm(prompt, system_message=None):
    """
    Call the local LLM at C:\jarvis
    Args:
        prompt (str): The prompt to send to the LLM
        system_message (str): Optional system message
    Returns:
        str: The response from the LLM
    """
    try:
        jarvis_path = Path("C:/jarvis")
        
        # Combine system message and prompt if provided
        full_prompt = f"{system_message}\n\n{prompt}" if system_message else prompt
        
        # Assuming your LLM has a command-line interface
        result = subprocess.run(
            [str(jarvis_path / "run.exe"), "--prompt", full_prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        logger.error(f"Error calling local LLM: {str(e)}")
        return f"Error: {str(e)}"

# Modify the process_with_ollama function
def process_with_ollama(prompt, system_message=None):
    """
    Process query using local LLM.
    Args:
        prompt (str): User query
        system_message (str): System message for context
    Returns:
        str: Generated response
    """
    try:
        return call_local_llm(prompt, system_message)
    except Exception as e:
        logger.error(f"Error processing with local LLM: {str(e)}")
        return f"Error: {str(e)}"

# Modify the process_with_groq function
def process_with_groq(prompt, system_message=None):
    """
    Process query using local LLM as fallback for Groq.
    Args:
        prompt (str): User query
        system_message (str): System message for context
    Returns:
        str: Generated response
    """
    try:
        return call_local_llm(prompt, system_message)
    except Exception as e:
        logger.error(f"Error processing with local LLM: {str(e)}")
        return f"Error: {str(e)}"


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

#def process_with_groq(prompt, system_message=None):
    """
    Process query using Groq API.
    Args:
        prompt (str): User query
        system_message (str): System message for context
    Returns:
        str: Generated response
    """
    try:
        if system_message is None:
            system_message = "You are a helpful AI assistant."
            
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True
        )
        
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
                
        return answer.strip()
    except Exception as e:
        logger.error(f"Error processing with Groq: {str(e)}")
        return f"Error: {str(e)}"

#def process_with_ollama(prompt, system_message=None):
    """
    Process query using Ollama LLM.
    Args:
        prompt (str): User query
        system_message (str): System message for context
    Returns:
        str: Generated response
    """
    try:
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        else:
            full_prompt = prompt
            
        response = ollama_model(full_prompt)
        return response
    except Exception as e:
        logger.error(f"Error processing with Ollama: {str(e)}")
        return f"Error: {str(e)}"

def save_chat_log(messages, file_path="data/processed_data/chat_log.json"):
    """
    Save chat log to a JSON file.
    Args:
        messages (list): List of message dictionaries
        file_path (str): Path to save the file
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(messages, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving chat log: {str(e)}")
