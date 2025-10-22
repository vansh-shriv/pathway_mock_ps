import re
from extract_utils import normalize_name


def names_similar(n1: str, n2: str) -> bool:
    # Simple name similarity: normalize and compare token sets.
    # This is rule-based and intentionally conservative.
    if not n1 or not n2:
        return False
    a = normalize_name(n1)
    b = normalize_name(n2)
    if a == b:
        return True
    a_tokens = set(a.split())
    b_tokens = set(b.split())
    # require substantial overlap
    inter = a_tokens.intersection(b_tokens)
    if len(inter) >= min(1, min(len(a_tokens), len(b_tokens))):
        return True
    return False

def compare_documents(doc_list: list) -> dict:
    # Given a list of extracted doc dicts, return a summary and flags.
    # doc dicts expected to have: doc_type, name, dob, id_number
    
    summary = { 'total_docs': len(doc_list), 'mismatches': [] }
    if not doc_list:
        return summary
    # pick first doc as reference
    ref = doc_list[0]
    for i, d in enumerate(doc_list[1:], start=1):
        # name check
        name_ok = names_similar(ref.get('name'), d.get('name'))
        dob_ok = (ref.get('dob') and d.get('dob') and ref.get('dob') == d.get('dob'))
        id_ok = (ref.get('id_number') and d.get('id_number') and ref.get('id_number') == d.get('id_number'))
        if not (name_ok and dob_ok and id_ok):
            summary['mismatches'].append({ 'index': i, 'doc': d, 'name_ok': name_ok, 'dob_ok': dob_ok, 'id_ok': id_ok })
    return summary