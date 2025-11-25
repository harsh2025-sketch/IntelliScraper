"""
IntelliScraper Setup Script
Automates the installation and configuration process
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header():
    print("=" * 60)
    print("  IntelliScraper - Setup Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_directories():
    """Create necessary directories"""
    print("\nCreating project directories...")
    directories = [
        "data",
        "data/raw_data",
        "data/processed_data",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        return False

def setup_env_file():
    """Create .env file if it doesn't exist"""
    print("\nSetting up environment file...")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping...")
        return
    
    env_template = """# API Keys (Replace with your actual keys)
OPENAI_API_KEY=your_openai_key_here
COHERE_API_KEY=your_cohere_key_here
GROQ_API_KEY=your_groq_key_here

# Configuration
Username=User
Assistantname=IntelliScraper
"""
    
    with open(".env", "w") as f:
        f.write(env_template)
    
    print("✅ Created .env file (remember to add your API keys)")

def check_ollama():
    """Check if Ollama is installed"""
    print("\nChecking for Ollama (optional)...")
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠️  Ollama not found (optional for local LLM)")
    print("   Download from: https://ollama.ai")
    return False

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python version requirement not met")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Setup .env file
    setup_env_file()
    
    # Check for Ollama
    check_ollama()
    
    # Final instructions
    print("\n" + "=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit .env file and add your API keys")
    print("2. (Optional) Install Ollama and run: ollama pull llama3")
    print("3. Start the application: streamlit run main.py")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
