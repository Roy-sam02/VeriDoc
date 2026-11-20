import json
import re
import sqlite3
import sys
from pathlib import Path

chunks_path = Path("data/processed/cuad_chunks.jsonl")
database_path = Path("data/processed/veridoc.sqlite3")

if len(sys.argv) < 2:
    raise SystemExit('Usage: python scripts/search.py "your question"')

question = " ".join(sys.argv[1:])
stopwords = {
    "what", "is", "the", "a", "an", "of", "in",
    "for", "does", "do", "this", "that", "and", "to",
}
terms = [
    word for word in re.findall(r"[a-z0-9]+", question.lower())
    if word not in stopwords
]

if not terms:
    raise SystemExit("Enter a question with at least one searchable word.")

fts_query = " OR ".join(f'"{term}"' for term in terms)

with sqlite3.connect(database_path) as db:
    db.execute("DROP TABLE IF EXISTS chunks")
    db.execute("""
        CREATE VIRTUAL TABLE chunks USING fts5(
            text,
            chunk_id UNINDEXED,
            document UNINDEXED,
            page UNINDEXED
        )
    """)

    count = 0
    with chunks_path.open(encoding="utf-8") as source:
        for line in source:
            chunk = json.loads(line)
            db.execute(
                "INSERT INTO chunks(text, chunk_id, document, page) "
                "VALUES (?, ?, ?, ?)",
                (
                    chunk["text"],
                    chunk["chunk_id"],
                    chunk["document"],
                    chunk["page"],
                ),
            )
            count += 1

    results = db.execute("""
        SELECT chunk_id, document, page, text, bm25(chunks) AS score
        FROM chunks
        WHERE chunks MATCH ?
        ORDER BY score
        LIMIT 3
    """, (fts_query,)).fetchall()

print(f"Indexed {count} chunks. Query terms: {terms}")

for position, (chunk_id, document, page, text, score) in enumerate(
    results, start=1
):
    print(f"\n--- Result {position} ---")
    print(f"Document: {document}")
    print(f"PDF page: {page}")
    print(f"Chunk ID: {chunk_id}")
    print(f"BM25 score: {score:.3f}")
    print(f"Full chunk:\n{text}")

if not results:
    print("No keyword matches found.")