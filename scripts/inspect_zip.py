import sys
import zipfile

with zipfile.ZipFile(sys.argv[1]) as archive:
    names = archive.namelist()
    pdfs = [name for name in names if name.lower().endswith(".pdf")]

    print("First 20 entries:")
    for name in names[:20]:
        print(name)

    print("PDF count:", len(pdfs))
    print("First 5 PDFs:")
    for name in pdfs[:5]:
        print(name)