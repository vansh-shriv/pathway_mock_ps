#!/bin/bash

# Start Ollama in background
ollama serve &

# Wait for Ollama to start
sleep 5

# Pull the model
ollama pull llama3.1:8b

# Start Streamlit
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
