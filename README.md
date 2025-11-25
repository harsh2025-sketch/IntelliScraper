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

- 🔍 **Multi-Mode**: URL scraping, Google search integration, interactive chat
- 🤖 **AI-Powered**: Extract structured data using LLM models
- 📊 **Data Export**: Save in JSON, CSV, and text formats
- 🛡️ **Anti-Bot**: Proxy support, user-agent rotation, intelligent delays
- 💬 **Interactive**: Query scraped data using natural language
- 📝 **Auto-Logging**: Comprehensive operation tracking

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/harsh2025-sketch/webscraper-3.0.git
cd webscraper-3.0

# Quick setup (Windows)
run.bat

# OR Manual setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
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

**URL Scraping**: Enter URL → Scrape → Describe extraction → Parse  
**Search Query**: Enter term → Enable auto-scrape → View AI analysis  
**Chat Mode**: Scrape data → Ask questions → Get AI answers

## 🏗️ Project Structure

```
IntelliScraper/
├── main.py           # Streamlit application
├── scrape.py         # Selenium + BeautifulSoup
├── parse.py          # AI parsing engine
├── model.py          # AI model integrations
├── utils.py          # Utilities & logging
├── requirements.txt  # Dependencies
└── setup.py         # Automated setup
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

## 👤 Author

**Harsh** • [@harsh2025-sketch](https://github.com/harsh2025-sketch)

---

<div align="center">

⭐ **Star this repo if you find it useful!** ⭐

Made with ❤️ by Harsh

</div>
