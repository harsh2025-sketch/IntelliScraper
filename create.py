import os

def create_project_structure(project_name):
    # Create project directory
    project_dir = project_name
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    
    # Create subdirectories
    subdirs = ["src", "data", "logs"]
    for subdir in subdirs:
        path = os.path.join(project_dir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
    
    # Create sub-subdirectories
    data_subdirs = ["raw_data", "processed_data"]
    for subdir in data_subdirs:
        path = os.path.join(project_dir, "data", subdir)
        if not os.path.exists(path):
            os.makedirs(path)
    
    # Create files
    files = {
        "src": ["__init__.py", "scrape.py", "parse.py", "model.py", "main.py", "utils.py"],
        "": [".env", "requirements.txt", "README.md"]
    }
    
    for dir_path, file_list in files.items():
        for file_name in file_list:
            file_path = os.path.join(project_dir, dir_path, file_name)
            if not os.path.exists(file_path):
                open(file_path, 'w').close()

def populate_files(project_name):
    # Populate .env file
    env_path = os.path.join(project_name, ".env")
    with open(env_path, 'w') as f:
        f.write("# Add your environment variables here\n")
        f.write("FIRECRAWL_API_KEY=\n")
        f.write("OPENAI_API_KEY=\n")
        f.write("COHERE_API_KEY=\n")
    
    # Populate requirements.txt
    req_path = os.path.join(project_name, "requirements.txt")
    with open(req_path, 'w') as f:
        f.write("selenium\n")
        f.write("beautifulsoup4\n")
        f.write("googlesearch\n")
        f.write("langchain\n")
        f.write("cohere\n")
        f.write("openai\n")
        f.write("python-dotenv\n")
    
    # Populate README.md
    readme_path = os.path.join(project_name, "README.md")
    with open(readme_path, 'w') as f:
        f.write("# Web Scraper 3.0\n")
        f.write("## Overview\n")
        f.write("This project is designed to perform real-time web scraping and data processing using AI models.\n")
        f.write("## Usage\n")
        f.write("1. Install dependencies from `requirements.txt`.\n")
        f.write("2. Configure environment variables in `.env`.\n")
        f.write("3. Run `main.py` to start the application.\n")

if __name__ == "__main__":
    project_name = "WebScraper3.0"
    create_project_structure(project_name)
    populate_files(project_name)
    print(f"Project structure for {project_name} created successfully.")
