import json
from collections import Counter
from pathlib import Path
from statistics import median

source = Path("data/processed/cuad_pages.jsonl")
records = [
    json.loads(line)
    for line in source.read_text(encoding="utf-8").splitlines()
]

if not records:
    raise ValueError(f"No page records found in {source}")

lengths = [len(record["text"].strip()) for record in records]
short_pages = [
    record for record in records
    if len(record["text"].strip()) < 100
]

print("Documents:", len({record["document"] for record in records}))
print("Pages:", len(records))
print("Characters per page (min/median/max):",
      min(lengths), int(median(lengths)), max(lengths))
print("Pages under 100 characters:", len(short_pages))

print("\nPages per document:")
for name, count in Counter(r["document"] for r in records).items():
    print(f"  {count:3}  {name}")

print("\nShort pages to inspect:")
for record in short_pages[:10]:
    print(
        f"  {record['document']} | page {record['page']} | "
        f"{len(record['text'].strip())} characters"
    )