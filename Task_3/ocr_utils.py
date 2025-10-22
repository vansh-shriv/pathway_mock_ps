from PIL import Image
import pytesseract
import fitz # PyMuPDF
from pathlib import Path
import tempfile
import numpy as np

def image_to_text(path: str) -> str:
    # Run OCR on an image file and return extracted text.
    img = Image.open(path).convert("RGB")
    # Basic pre-processing can be added here (grayscale, thresholding)
    text = pytesseract.image_to_string(img)
    return text

def pdf_to_text(path: str) -> str:
    # Extract images/text from PDF: convert pages to images and OCR them.
    doc = fitz.open(path)
    full_text = []
    for page in doc:
        # try to extract direct text first
        txt = page.get_text()
        if txt and txt.strip():
            full_text.append(txt)
            continue
        # otherwise render page as image and OCR
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("ppm")
        nparr = np.frombuffer(img_bytes, np.uint8)
        # PIL can read from bytes; but easiest to write to temp file
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            tmp.write(img_bytes)
            tmp.flush()
            ocr = pytesseract.image_to_string(Image.open(tmp.name))
            full_text.append(ocr)
    return "\n".join(full_text)


def file_to_text(path: str) -> str:
    p = Path(path)
    suf = p.suffix.lower()
    if suf in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
        return image_to_text(str(path))
    if suf in ['.pdf']:
        return pdf_to_text(str(path))
    # fallback: read as text file
    return p.read_text(encoding='utf-8', errors='ignore')