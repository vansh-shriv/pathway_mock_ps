import re
from dateutil import parser

def normalize_name(name: str) -> str:
    if not name:
        return ''
    s = re.sub(r"[^A-Za-z\s]", "", name).strip().upper()
    s = re.sub(r"\s+", " ", s)
    return s


def extract_pan(text: str) -> dict:
    # Extract PAN-like fields from free text. PAN in India is a 10-character alphanumeric (e.g., ABCDE1234F).
    # Also try to capture NAME and DOB lines nearby using simple heuristics.
    
    res = {'doc_type': 'PAN', 'name': None, 'dob': None, 'id_number': None}
    # PAN pattern
    pan_match = re.search(r"\b([A-Z]{5}[0-9]{4}[A-Z])\b", text)
    if pan_match:
        res['id_number'] = pan_match.group(1)
    # NAME heuristics: find lines with 'Name' or uppercase sequences
    name_match = re.search(r"Name[:\s]+([A-Z\s]{3,100})", text, flags=re.IGNORECASE)
    if name_match:
        res['name'] = name_match.group(1).strip()
    else:
        # fallback: first long uppercase line
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for l in lines[:8]:
            if re.match(r"^[A-Z\s]{4,}$", l):
                res['name'] = l
                break
    # DOB pattern (common formats)
    dob_match = re.search(r"(\d{2}[-/.]\d{2}[-/.]\d{4})", text)
    if dob_match:
        try:
            res['dob'] = str(parser.parse(dob_match.group(1)).date())
        except Exception:
            res['dob'] = dob_match.group(1)
    return res




def extract_aadhar(text: str) -> dict:
    # Extract basic fields from Aadhar-like text.
    # Aadhar numbers are 12-digit numeric sequences often grouped as 4-4-4.
    res = {'doc_type': 'AADHAAR', 'name': None, 'dob': None, 'id_number': None}
    # Aadhaar number
    a_match = re.search(r"\b(\d{4}\s?\d{4}\s?\d{4})\b", text)
    if a_match:
        res['id_number'] = re.sub(r"\s+", "", a_match.group(1))
    # Name heuristics
    name_match = re.search(r"Name[:\s]+([A-Z\s]{3,100})", text, flags=re.IGNORECASE)
    if name_match:
        res['name'] = name_match.group(1).strip()
    else:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for l in lines[:10]:
            if re.match(r"^[A-Z\s]{3,}$", l):
            # skip lines like 'GOVERNMENT OF INDIA'
                if len(l.split()) < 6:
                    res['name'] = l
                    break
    # DOB patterns: often 'DOB: DD-MM-YYYY' or 'Year of Birth'
    dob_match = re.search(r"DOB[:\s]*(\d{2}[-/.]\d{2}[-/.]\d{4})", text, flags=re.IGNORECASE)
    if not dob_match:
        dob_match = re.search(r"(\d{2}[-/.]\d{2}[-/.]\d{4})", text)
    if dob_match:
        try:
            res['dob'] = str(parser.parse(dob_match.group(1)).date())
        except Exception:
            res['dob'] = dob_match.group(1)
    return res




def generic_extract(text: str) -> dict:
    # Try both PAN and Aadhaar extractors and return the best match.
    a = extract_aadhar(text)
    p = extract_pan(text)
    # prefer the one with an id_number
    if a.get('id_number'):
        return a
    if p.get('id_number'):
        return p
    # fallback: merge heuristics
    merged = {'doc_type': 'UNKNOWN', 'name': a.get('name') or p.get('name'), 'dob': a.get('dob') or p.get('dob'), 'id_number': a.get('id_number') or p.get('id_number')}
    return merged