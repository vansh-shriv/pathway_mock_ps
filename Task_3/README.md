````markdown
# Smart KYC Checker — Quick Run

## Setup
1. Install system Tesseract (or use Docker provided)
2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
````

## Run locally

Provide one or more document paths (images or PDF):

```bash
python main.py sample_docs/aadhar.jpg sample_docs/pan.jpg
```

The program will:

* OCR each file (if image/pdf)
* Extract name/dob/id using heuristics
* Compare documents and produce a mismatch summary
* Display extracted records using Pathway debug table

## Docker

Build and run the Docker image (Tesseract included):

```bash
docker build -t kyc-checker .
docker run --rm -v "$(pwd):/app" kyc-checker python main.py sample_docs/sample_aadhar.png sample_docs/sample_PAN.png
```

---

```

---
