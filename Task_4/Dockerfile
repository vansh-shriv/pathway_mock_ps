FROM python:3.11-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py llm_handler.py database.py entity_extractor.py ./

# Create data directory
RUN mkdir -p /app/data

# Expose ports
EXPOSE 8501 11434

# Copy and set executable permissions for start script
COPY start.sh .
RUN chmod +x start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["./start.sh"]
