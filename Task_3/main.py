import argparse
from pathlib import Path
from ocr_utils import file_to_text
from extract_utils import generic_extract, normalize_name
from fraud_check import compare_documents
import pathway as pw
import pandas as pd




def build_markdown_table(docs):
    """Create a simple markdown table for Pathway debug printing."""
    hdr = "doc_type | name | dob | id_number"
    rows = [hdr, "--- | --- | --- | ---"]
    for d in docs:
        # Escape any pipe characters and properly handle empty values
        doc_type = str(d.get('doc_type', '')).strip().replace('|', '\\|') or '-'
        name = str(d.get('name', '')).strip().replace('|', '\\|') or '-'
        dob = str(d.get('dob', '')).strip().replace('|', '\\|') or '-'
        id_number = str(d.get('id_number', '')).strip().replace('|', '\\|') or '-'
        # Add quotes around fields that might contain spaces
        row = f'"{doc_type}" | "{name}" | "{dob}" | "{id_number}"'
        rows.append(row)
    return "\n".join(rows)


def main(args):
    paths = args.files
    docs = []
    for p in paths:
        text = file_to_text(p)
        info = generic_extract(text)
        # normalize and keep raw text snippet for debugging
        info['name'] = normalize_name(info.get('name') or '')
        info['source'] = p
        # Only keep the fields we need for the table
        info_filtered = {
            'doc_type': info.get('doc_type', ''),
            'name': info.get('name', ''),
            'dob': info.get('dob', ''),
            'id_number': info.get('id_number', '')
        }
        docs.append(info_filtered)

    summary = compare_documents(docs)

    # Debug print to see what's going into the table
    print("\nDocument data before table creation:")
    for doc in docs:
        print(doc)

    # Prepare a small human-friendly output using Pathway debug table
    md = build_markdown_table(docs)
    print("\nMarkdown table content:")
    print(md)
    table = pw.debug.table_from_markdown(md)
    print("\n=== Extracted Info (Pathway debug table) ===\n")
    pw.debug.compute_and_print(table)


    print("\n=== Fraud Summary ===\n")
    print(summary)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='Paths to document image/pdf/text files')
    args = parser.parse_args()
    main(args)