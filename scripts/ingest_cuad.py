import argparse
import json
import shutil
import zipfile
from pathlib import Path

import pymupdf


def ingest(archive_path: Path, limit: int = 5) -> None:
    raw_dir = Path("data/raw/cuad")
    processed_dir = Path("data/processed")
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_path = processed_dir / "cuad_pages.jsonl"

    documents = 0
    pages = 0
    empty_pages = 0

    with zipfile.ZipFile(archive_path) as archive:
        pdfs = sorted(
            (
                item
                for item in archive.infolist()
                if not item.is_dir()
                and item.filename.lower().endswith(".pdf")
                and "full_contract_pdf/" in item.filename.lower()
                and item.file_size <= 15_000_000
            ),
            key=lambda item: item.filename,
        )

        if not pdfs:
            raise ValueError("No CUAD contract PDFs found in this ZIP.")

        with output_path.open("w", encoding="utf-8") as output:
            for number, item in enumerate(pdfs[:limit], start=1):
                filename = f"{number:03d}_{Path(item.filename).name}"
                pdf_path = raw_dir / filename

                with archive.open(item) as source, pdf_path.open("wb") as target:
                    shutil.copyfileobj(source, target)

                with pymupdf.open(str(pdf_path)) as document:
                    page_count = len(document)

                    for page_number, page in enumerate(document, start=1):
                        text = page.get_text("text")
                        record = {
                            "source_dataset": "CUAD v1",
                            "archive_member": item.filename,
                            "document": filename,
                            "page": page_number,
                            "text": text,
                        }
                        output.write(json.dumps(record, ensure_ascii=False) + "\n")
                        pages += 1
                        if not text.strip():
                            empty_pages += 1

                documents += 1
                print(f"Read {filename}: {page_count} pages")

    print(f"Saved {documents} PDFs and {pages} page records.")
    print(f"Pages with no extracted text: {empty_pages}")
    print(f"Page records: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    arguments = parser.parse_args()
    ingest(arguments.archive)