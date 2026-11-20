import json
from pathlib import Path

source = Path("data/processed/cuad_pages.jsonl")
destination = Path("data/processed/cuad_chunks.jsonl")

chunk_size = 120
step = 100
total = 0

with source.open(encoding="utf-8") as input_file, \
     destination.open("w", encoding="utf-8") as output_file:

    for line in input_file:
        page = json.loads(line)
        words = page["text"].split()

        for start in range(0, len(words), step):
            # Stop if the previous chunk already contains all remaining words.
            if start > 0 and start - step + chunk_size >= len(words):
                break

            selected = words[start:start + chunk_size]
            if not selected:
                continue

            chunk = {
                "chunk_id": f"{page['document']}|p{page['page']}|w{start}",
                "document": page["document"],
                "page": page["page"],
                "start_word": start,
                "text": " ".join(selected),
            }
            output_file.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            total += 1

print(f"Created {total} chunks in {destination}")