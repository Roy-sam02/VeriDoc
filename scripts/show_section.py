import re
from pathlib import Path

import pymupdf

folder = Path("data/raw/cuad")
matches = list(folder.glob("003_*.pdf"))

if len(matches) != 1:
    raise ValueError(f"Expected one 003 PDF, found {len(matches)}")

pdf_path = matches[0]
page_number = 21  # PDF page number, starting at 1

with pymupdf.open(str(pdf_path)) as pdf:
    text = pdf[page_number - 1].get_text("text", sort=True)

start = re.search(r"Section\s+8\.3\b", text, flags=re.IGNORECASE)
if start is None:
    raise ValueError("Section 8.3 was not found on PDF page 21")

end = re.search(r"Section\s+8\.4\b", text[start.end():],
                flags=re.IGNORECASE)

section_end = start.end() + end.start() if end else len(text)

print(f"Document: {pdf_path.name}")
print(f"PDF page: {page_number}")
print("\n" + text[start.start():section_end].strip())

if end is None:
    print("\n[Section 8.4 was not found on this page; "
          "Section 8.3 may continue on the next page.]")