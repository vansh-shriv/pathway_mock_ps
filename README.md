# FinanceBot - AI-Powered Customer Support

An AI chatbot for financial customer support using local LLM (Llama 3.1).

## Features
- ✅ Natural language financial query handling
- ✅ Local LLM (no API costs)
- ✅ Automatic entity extraction (name, email, phone)
- ✅ Conversation history storage
- ✅ Dockerized deployment

## Requirements
- Docker Desktop
- WSL2 (for Windows)
- 8GB RAM minimum

## Installation & Running

### Option 1: Run with Docker (Recommended)
```bash
docker-compose up --build
```
Access at: http://localhost:8501

### Option 2: Run Locally
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve &

# Pull model
ollama pull llama3.1:8b

# Install Python dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## Usage
1. Open the app in browser
2. Start asking financial questions
3. Share your details in conversation to build your profile
4. View extracted information in the sidebar

## Architecture
- **Frontend**: Streamlit
- **LLM**: Ollama (Llama 3.1)
- **Database**: SQLite
- **NLP**: spaCy for entity extraction

## Project Structure
```
financial-chatbot/
├── app.py                 # Main Streamlit application
├── llm_handler.py         # LLM interaction logic
├── database.py            # SQLite database operations
├── entity_extractor.py    # Entity extraction logic
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── requirements.txt       # Python dependencies
└── data/                  # Database storage
```

## Author
[Your Name]
