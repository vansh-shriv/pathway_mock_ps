#!/bin/bash
set -e

echo "🚀 Starting Ollama service..."
ollama serve &

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to start..."
sleep 10

# Check if Ollama is responding
until curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "⏳ Waiting for Ollama API..."
    sleep 5
done

echo "✅ Ollama is ready!"

# Pull the model
echo "📥 Pulling Llama 3.1 model (this may take a few minutes on first run)..."
ollama pull llama3.1:8b

echo "✅ Model downloaded!"

# Start Streamlit
echo "🌟 Starting Streamlit app..."
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false