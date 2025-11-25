import os
import logging
import json
from datetime import datetime
import csv
import pandas as pd

def save_csv(data, filename, folder="data"):
    """
    Save data as CSV.
    
    Args:
        data (list): List of dictionaries to save
        filename (str): Name of the file
        folder (str): Folder to save the file in (default: "data")
        
    Returns:
        str: Path to the saved file
    """
    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Full path to the file
    file_path = os.path.join(folder, filename)
    
    try:
        # Convert to DataFrame and save
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        return file_path
    except Exception as e:
        logging.error(f"Error saving CSV: {str(e)}")
        
        # Fallback to manual CSV writing if pandas fails
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                if data and isinstance(data[0], dict):
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    writer = csv.writer(f)
                    writer.writerows(data)
            return file_path
        except Exception as e2:
            logging.error(f"Fallback CSV saving also failed: {str(e2)}")
            return None


def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration for the application.
    Args:
        log_level (int): Logging level (default: logging.INFO)
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Set up logging format and handlers
    log_filename = f"logs/webscraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    # Return logger for the module
    return logging.getLogger(__name__)

def save_data(data, filename, folder="data"):
    """
    Save data to a file.
    Args:
        data (str): Data to save
        filename (str): Name of the file
        folder (str): Folder to save the file in (default: "data")
    """
    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Full path to the file
    file_path = os.path.join(folder, filename)
    
    # Save the data
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
    
    return file_path

def load_data(filename, folder="data"):
    """
    Load data from a file.
    Args:
        filename (str): Name of the file
        folder (str): Folder where the file is located (default: "data")
    Returns:
        str: The content of the file
    """
    # Full path to the file
    file_path = os.path.join(folder, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        return None
    
    # Load the data
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_json(data, filename, folder="data"):
    """
    Save data as JSON.
    Args:
        data (dict): Data to save
        filename (str): Name of the file
        folder (str): Folder to save the file in (default: "data")
    """
    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Full path to the file
    file_path = os.path.join(folder, filename)
    
    # Save the data
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    return file_path

def load_json(filename, folder="data"):
    """
    Load JSON data from a file.
    Args:
        filename (str): Name of the file
        folder (str): Folder where the file is located (default: "data")
    Returns:
        dict: The content of the file as a dictionary
    """
    # Full path to the file
    file_path = os.path.join(folder, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        return None
    
    # Load the data
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_timestamp():
    """
    Get a formatted timestamp.
    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def clean_filename(filename):
    """
    Clean a filename by removing invalid characters.
    Args:
        filename (str): Filename to clean
    Returns:
        str: Cleaned filename
    """
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename
