import json
import re
from pathlib import Path

source = Path("data/processed/cuad_pages.jsonl")
matches = []

with source.open(encoding="utf-8") as file:
    for line in file:
        page = json.loads(line)

        if not page["document"].startswith("003_"):
            continue

        section = re.search(
            r"Section\s+8\.3\b(.*?)Section\s+8\.4\b",
            page["text"],
            flags=re.IGNORECASE | re.DOTALL,
        )
        if section is None:
            continue

        clean_text = " ".join(section.group(1).split())
        finding = re.search(
            r"NCM may terminate this Agreement.*?"
            r"permanently discontinued\.",
            clean_text,
            flags=re.IGNORECASE,
        )
        if finding:
            matches.append((page, finding.group(0)))

if len(matches) != 1:
    print("Insufficient evidence: expected one complete Section 8.3 finding.")
else:
    page, answer = matches[0]
    print("Finding:", answer)
    print("Document:", page["document"])
    print("PDF page:", page["page"])
    print("Section: 8.3")