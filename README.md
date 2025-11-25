# 🧠 IntelliScraper

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-Powered Web Scraping & Analysis Platform**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage)

</div>

---

## 📋 Overview

**IntelliScraper** is an advanced AI-powered web scraping tool combining real-time search, intelligent content extraction, and interactive data querying. Built with Streamlit and integrated with multiple AI models (Ollama, Groq, OpenAI, Cohere).

## ✨ Features

- 🔍 **Simple Interface**: Clean, intuitive Streamlit UI
- 🤖 **AI-Powered**: Extract structured data using LLM models
- 📊 **Auto-Save**: All data automatically saved
- 🛡️ **Anti-Bot**: User-agent rotation, intelligent delays
- 💾 **Local Storage**: Data saved in organized folders
- 📝 **Logging**: Track all operations

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/harsh2025-sketch/webscraper-3.0.git
cd webscraper-3.0

# Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

## 🔧 Prerequisites

- Python 3.8+
- Chrome/Chromium browser
- API Keys (optional): OpenAI, Cohere, Groq

## 📦 Configuration

Create `.env` file:
```env
OPENAI_API_KEY=your_key
COHERE_API_KEY=your_key
GROQ_API_KEY=your_key
```

## 💡 Usage

**Simple 2-Step Process:**
1. Enter website URL → Click "Scrape Website"
2. Describe what to extract → Click "Extract"

All data is automatically saved in the `data/` folder.

## 🏗️ Project Structure

```
IntelliScraper/
├── main.py           # Simple Streamlit UI
├── scrape.py         # Web scraping engine
├── parse.py          # AI parsing
├── model.py          # AI models
├── utils.py          # Utilities
├── requirements.txt  # Dependencies
└── setup.py         # Setup script
```

## 📊 Data Storage

- **Raw**: `data/raw_data/`
- **Processed**: `data/processed_data/`
- **Logs**: `logs/`

## 🛠️ Advanced Features

- Automatic ChromeDriver management
- Exponential backoff retry logic
- Content chunking for large documents
- Real-time query categorization
- Structured data extraction

## 🐛 Troubleshooting

**Import errors**: `pip install -r requirements.txt`  
**ChromeDriver**: Auto-downloaded, ensure Chrome installed  
**Ollama**: Install from [ollama.ai](https://ollama.ai) → `ollama pull llama3`

## 🤝 Contributing

Fork → Create branch → Commit → Push → Pull Request

## 📄 License

MIT License
---

<div align="center">

⭐ **Star this repo if you find it useful!** ⭐


</div>
